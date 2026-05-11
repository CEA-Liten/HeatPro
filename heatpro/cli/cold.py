import logging
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.table import Table

from .. import COLD_OPERATING_MONTHS


def cold_cli(weather_csv: Path, year_energy_reference: float, set_temperature: float) -> None:
    console = Console()
    weather = pd.read_csv(
        weather_csv,
        sep=";",
        index_col="timestamp_utc_num",
        usecols=["timestamp_utc_num", "temperature"],
        dtype={"temperature": float},
        decimal=",",
    )["temperature"]
    weather.index = pd.to_datetime(weather.index, unit="s")
    weather = weather.loc[:"2022"]

    reference_delta_temperature: float = (
        (weather.loc[weather.index.month.isin(COLD_OPERATING_MONTHS)] - set_temperature)
        .clip(0)
        .resample("YS")
        .mean()
        .mean()
    )
    logging.debug(f"{reference_delta_temperature=}")
    year_average_power = (
        (weather.loc[weather.index.month.isin(COLD_OPERATING_MONTHS)] - set_temperature)
        .clip(0)
        .resample("YS")
        .mean()
        / reference_delta_temperature
        * year_energy_reference
        / weather.resample("YS").count()
    ).rename("year_average_power_kW")

    table = Table(show_header=True, header_style="bold magenta")

    table.add_column(weather.index.name)
    table.add_column(weather.name)

    for index, value in weather.sample(5).items():
        table.add_row(index.strftime("%Y-%m-%d %H:%M"), str(value))

    year_power_table = Table(show_header=True, header_style="bold magenta")

    year_power_table.add_column(year_average_power.index.name)
    year_power_table.add_column(year_average_power.name)

    for index, value in year_average_power.head(5).items():
        year_power_table.add_row(index.strftime("%Y-%m-%d %H:%M"), str(value))

    console.print(f"{year_energy_reference=}")
    console.print(table)
    console.print(year_power_table)
