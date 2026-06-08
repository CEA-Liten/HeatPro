"""Cold module for calculating cold-related energy consumption.

This module provides functionality to calculate cold-related energy consumption
based on weather data and configuration parameters. It includes functions for
importing weather data, calculating year average power, and applying cold
configuration to generate consumption data.

The module uses pandas for data manipulation and analysis, and includes
functions for calculating felt temperature and applying week profiles to the data.
"""

from dataclasses import dataclass, field
import logging
import math
from pathlib import Path

import pandas as pd

from .. import COLD_OPERATING_MONTHS, SET_TEMPERATURE_COLD
from ..cold.distribution import (
    year_to_hour_outdoor_temperarure_distribution,
)

from ..cold.standard_profile import StandardProfile
from ..felt_temperature import calculate_felt_temperature
from ..week_profile import apply_week_profile


def import_weather(weather_csv: Path) -> pd.Series:
    """Import weather data from a CSV file.

    CSV should look like this (more columns are allow but will be ignored):

    ::

        "timestamp_utc_num";"temperature";
        978307200;5,1
        978310800;5,1
        978314400;5

    Args:
        weather_csv (Path): Path to the CSV file containing weather data.

    Returns:
        pd.Series: A pandas Series containing temperature (°C) at hourly frequency data indexed by timestamp.

    Example:
        >>> weather_data = import_weather(Path("./data/weather_data.csv"))
    """
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
    r"""Calculate the year average power based on weather data and a year energy reference.

    Year energy reference will be the average year consumption over the all weather period
    given (it can be multiple years).

    Mathematically, we define :math:`\mathcal{T}` datetime index from ``weather.index``,
    :math:`T_{ext}^t` outdoor temperature from ``weather``,
    :math:`E_{ref}` year energy reference from ``year_energy_reference``,
    :math:`T_{set}` cooling set temperature in buildings from ``set_temperature``,

    We defined for a year math:`y \in \mathcal{T}` the average delta temperature during summer:

    .. math::

        \Delta^{(y)} = \frac{1}{|\text{summer of }y|}\sum_{t\in \text{summer of }y} ( T_{ext}^{(t)}-T_{set} ) _+

    The higher this value, the higher will be the cold energy demand.

    We calculate the average over ther year of the average delta temperature during summer:

    .. math::

        \Delta_{ref} = \frac{1}{\#\text{years in }\mathcal{T}}\sum_{y\in\mathcal{T}} \Delta^{(y)}

    We can now estimate annual energy demand :math:`E^{(y)}` for each year :math:`y` using cross product:

    .. math::

        E^{(y)} = \frac{E_{ref}}{\Delta_{ref}} \cdot \Delta^{(y)}

    On average yearly demand will be :math:`E_{ref}`.

    Eventually, average yearly power is calculated and return:

    .. math::

        P^{(y)} = \frac{E^{(y)}}{|y|}

    Args:
        weather (pd.Series): A pandas Series containing temperature data.
        year_energy_reference (float): Reference energy value for the year.
        set_temperature (float): Set temperature for cold calculation.

    Returns:
        pd.Series: A pandas Series containing the calculated year average power.

    Example:
        >>> year_avg_power = calculate_year_average_power(weather_data, 1000.0, 18.0)
    """
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
    """Class representing the repartition of values.

    Attributes:
        full_week (float): Value for full week. Defaults to 0.5.
        working_day (float): Value for working fay. Defaults to 0.5.
    """

    full_week: float = 0.5
    working_day: float = 0.5


@dataclass
class ColdConfig:
    """Configuration class for cold calculations.

    Attributes:
        set_temperature (float): Set temperature for cold calculation.
        loss (float): Loss factor. Defaults to 0.2.
        profile (Repartition): Repartition profile. Defaults to Repartition().
        temperature_sensitivity (Repartition): Temperature sensitivity profile.
            Defaults to Repartition().

    Raises:
        ValueError: If the sum of profile values is not 1.0.
        ValueError: If temperature_sensitivity values are not between 0 and 1.
    """

    set_temperature: float = SET_TEMPERATURE_COLD
    loss: float = 0.2
    profile: Repartition = field(default_factory=Repartition)
    temperature_sensitivity: Repartition = field(default_factory=Repartition)

    def __post_init__(self):
        """Post-initialization method to validate configuration."""
        if not math.isclose(self.profile.full_week + self.profile.working_day, 1.0):
            raise ValueError("The sum of profile values must equal 1.0")
        if not (0 <= self.temperature_sensitivity.full_week <= 1):
            raise ValueError("temperature_sensitivity.full_week must be between 0 and 1")
        if not (0 <= self.temperature_sensitivity.working_day <= 1):
            raise ValueError("temperature_sensitivity.working_day must be between 0 and 1")


def cold_pipeline(
    weather: pd.Series, year_energy_reference: float, config: ColdConfig
) -> pd.DataFrame:
    """Calculate cold-related energy consumption based on weather data and configuration.

    Args:
        weather (pd.Series): A pandas Series containing temperature data.
        year_energy_reference (float): Reference energy value for the year.
        config (ColdConfig): Configuration object for cold calculations.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the calculated cold-related consumption.

    Example:
        >>> config = ColdConfig(set_temperature=18.0)
        >>> consumption_data = cold_cli(weather_data, 1000.0, config)
    """
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
            * config.profile.working_day
            * (1 - config.temperature_sensitivity.working_day)
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
        (year_average_power * config.profile.working_day * config.temperature_sensitivity.working_day)
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
    result["total_consumption_power"] = result.loc[:, result.columns != weather.name].sum(axis=1)
    result.index = weather.index.astype("datetime64[s]").astype("int64")

    return result
