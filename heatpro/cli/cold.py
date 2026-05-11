import logging
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from rich.console import Console
from rich.table import Table

from .. import COLD_OPERATING_MONTHS
from ..cold.distribution import (
    year_to_hour_outdoor_temperarure_distribution,
)
from ..cold.standard_profile import StandardProfile
from ..felt_temperature import calculate_felt_temperature
from ..week_profile import apply_week_profile


def import_weather(weather_csv: Path) -> pd.Series:
    weather = pd.read_csv(
        weather_csv,
        sep=";",
        index_col="timestamp_utc_num",
        usecols=["timestamp_utc_num", "temperature"],
        dtype={"temperature": float},
        decimal=",",
    )["temperature"]
    weather.index = pd.to_datetime(weather.index, unit="s")
    return weather


def calculate_year_average_power(
    weather: pd.Series, year_energy_reference: float, set_temperature: float
) -> pd.Series:
    reference_delta_temperature: float = (
        (weather.loc[weather.index.month.isin(COLD_OPERATING_MONTHS)] - set_temperature)
        .clip(0)
        .resample("YS")
        .mean()
        .mean()
    )
    logging.debug(f"{reference_delta_temperature=}")
    return (
        (weather.loc[weather.index.month.isin(COLD_OPERATING_MONTHS)] - set_temperature)
        .clip(0)
        .resample("YS")
        .mean()
        / reference_delta_temperature
        * year_energy_reference
        / weather.resample("YS").count()
    ).rename("year_average_power_kW")


def cold_cli(weather: pd.Series, year_energy_reference: float, set_temperature: float) -> None:
    console = Console()

    weather = weather.loc[:"2002"]
    logging.debug(f"weather series description:\n{weather.describe()}")
    logging.debug(
        f"weather series index:\n - start : {weather.index.min()}\n - end : {weather.index.max()}"
    )

    year_average_power = calculate_year_average_power(
        weather, year_energy_reference, set_temperature
    )
    loss_year_average_power = (
        (year_average_power * 0.02)
        .reindex(weather.index, method="ffill")
        .rename("loss_year_average_power")
    )
    working_day_baseload_year_average_power = (
        (year_average_power / 4)
        .reindex(weather.index, method="ffill")
        .rename("working_day_baseload_year_average_power")
    )
    full_week_baseload_year_average_power = (
        (year_average_power / 4)
        .reindex(weather.index, method="ffill")
        .rename("full_week_baseload_year_average_power")
    )
    working_day_temperature_sensitive_year_average_power = (
        (year_average_power / 4)
        .reindex(weather.index, method="ffill")
        .rename("working_day_temperature_sensitive_year_average_power")
    )
    full_week_temperature_sensitive_year_average_power = (
        (year_average_power / 4)
        .reindex(weather.index, method="ffill")
        .rename("full_week_temperature_sensitive_year_average_power")
    )

    felt_temperature = calculate_felt_temperature(weather)

    operating_season = pd.Series(
        weather.index.month.isin(COLD_OPERATING_MONTHS).astype(int),
        index=weather.index,
        name="operating_season",
    )

    full_week_profile_weigths = apply_week_profile(
        weather.index,
        lambda day, hour: StandardProfile.FULL_WEEK.value.function(day, hour),
    )
    working_day_profile_weigths = apply_week_profile(
        weather.index,
        lambda day, hour: StandardProfile.WORKING_DAY.value.function(day, hour),
    )

    full_week_baseload_year_average_power_series = (
        full_week_baseload_year_average_power
        * full_week_profile_weigths
        / full_week_profile_weigths.mean()
    ).rename(full_week_baseload_year_average_power.name)
    working_day_baseload_year_average_power_series = (
        working_day_baseload_year_average_power
        * working_day_profile_weigths
        / working_day_profile_weigths.mean()
    ).rename(working_day_baseload_year_average_power.name)

    full_week_temperature_sensitive_year_average_power_series = (
        year_to_hour_outdoor_temperarure_distribution(
            full_week_temperature_sensitive_year_average_power,
            felt_temperature,
            full_week_profile_weigths * operating_season,
        )
    )
    working_day_temperature_sensitive_year_average_power_series = (
        year_to_hour_outdoor_temperarure_distribution(
            working_day_temperature_sensitive_year_average_power,
            felt_temperature,
            working_day_profile_weigths * operating_season,
        )
    )

    result = pd.concat(
        (
            weather,
            loss_year_average_power,
            working_day_baseload_year_average_power_series,
            full_week_baseload_year_average_power_series,
            working_day_temperature_sensitive_year_average_power_series,
            full_week_temperature_sensitive_year_average_power_series,
        ),
        axis=1,
    )
    result.index = weather.index.astype("int64") // 10**9  # 10**9 convert nanoseconde to second

    result.to_csv("./results.csv", sep=";", float_format="%.2f")
