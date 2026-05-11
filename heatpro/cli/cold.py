from dataclasses import dataclass, field
import logging
import math
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from rich.console import Console

from .. import COLD_OPERATING_MONTHS, SET_TEMPERATURE_COLD
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


@dataclass
class Repartition:
    full_week: float = 0.5
    week_start: float = 0.5


@dataclass
class ColdConfig:
    set_temperature: float = SET_TEMPERATURE_COLD
    loss: float = 0.2
    profile: Repartition = field(default_factory=Repartition)
    temperature_sensitivity: Repartition = field(default_factory=Repartition)

    def __post_init__(self):
        if not math.isclose(self.profile.full_week + self.profile.week_start, 1.0):
            raise ValueError("The sum of profile values must equal 1.0")
        if not (0 <= self.temperature_sensitivity.full_week <= 1):
            raise ValueError("temperature_sensitivity.full_week must be between 0 and 1")
        if not (0 <= self.temperature_sensitivity.week_start <= 1):
            raise ValueError("temperature_sensitivity.week_start must be between 0 and 1")


def cold_cli(weather: pd.Series, year_energy_reference: float, config: ColdConfig) -> pd.DataFrame:
    weather = weather.loc[:"2022"]
    logging.debug(f"weather series description:\n{weather.describe()}")
    logging.debug(
        f"weather series index:\n - start : {weather.index.min()}\n - end : {weather.index.max()}"
    )

    year_average_power = calculate_year_average_power(
        weather, year_energy_reference, config.set_temperature
    )
    loss_year_average_power = (
        (year_average_power * config.loss)
        .reindex(weather.index, method="ffill")
        .rename("loss_year_average_power")
    )
    working_day_baseload_year_average_power = (
        (
            year_average_power
            * config.profile.week_start
            * (1 - config.temperature_sensitivity.week_start)
        )
        .reindex(weather.index, method="ffill")
        .rename("working_day_baseload_year_average_power")
    )
    full_week_baseload_year_average_power = (
        (
            year_average_power
            * config.profile.full_week
            * (1 - config.temperature_sensitivity.full_week)
        )
        .reindex(weather.index, method="ffill")
        .rename("full_week_baseload_year_average_power")
    )
    working_day_temperature_sensitive_year_average_power = (
        (year_average_power * config.profile.week_start * config.temperature_sensitivity.week_start)
        .reindex(weather.index, method="ffill")
        .rename("working_day_temperature_sensitive_year_average_power")
    )
    full_week_temperature_sensitive_year_average_power = (
        (year_average_power * config.profile.full_week * config.temperature_sensitivity.full_week)
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

    return result
    
