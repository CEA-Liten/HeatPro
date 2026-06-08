import pandas as pd

from .check import ENERGY_FEATURE_NAME
from .demand_profile import WEIGHT_NAME_REQUIRED
from .external_factors import (
    ExternalFactors,
    burch_cold_water,
    closed_heating_season,
    CLOSED_HEATING_SEASON_NAME,
)
from .temporal_demand import HourlyHeatDemand


def special_hot_water(
    external_factors: ExternalFactors,
    total_heating_including_hotwater: pd.Series,
    monthly_hot_water_profile: pd.DataFrame,
    temperature_hot_water: float,
    hourly_hot_water_day_profil: pd.Series,
    name: str = "hot_water",
):
    """Calculate the hourly energy demand for hot water considering external factors and profiles.

    Args:
        external_factors (ExternalFactors): Object containing external factors affecting hot water energy demand.
        total_heating_including_hotwater (pd.Series): Monthly total heat demand including hot water.
        monthly_hot_water_profile (pd.DataFrame): Monthly hot water profile (In term of quantity i.e. L).
        temperature_hot_water (float): The temperature of the hot water.
        hourly_hot_water_day_profil (pd.Series): Hourly profile for hot water demand (In term of quantity i.e. L).
        name (str, optional): Name of the demand. Defaults to "hot_water".

    Returns:
        HourlyHeatDemand: The hourly demand for hot water.
    """

    # Calculate induced factors based on external factors
    induced_factors = pd.concat(
        (
            closed_heating_season(external_factors),
            burch_cold_water(external_factors),
        ),
        axis=1,
    )

    # Calculate hourly hot water profile weighted by day length
    hourly_hot_water_month_profile = (
        (monthly_hot_water_profile / 24).reindex(induced_factors.index).ffill()
    )

    # Calculate non-heating season consumption
    non_heating_season_consumption = total_heating_including_hotwater[
        ~induced_factors[CLOSED_HEATING_SEASON_NAME].reindex(total_heating_including_hotwater.index)
    ].sum()

    df = pd.DataFrame(
        {
            "Year": total_heating_including_hotwater[
                ~induced_factors[CLOSED_HEATING_SEASON_NAME].reindex(
                    total_heating_including_hotwater.index
                )
            ].index.year,
            "Month": total_heating_including_hotwater[
                ~induced_factors[CLOSED_HEATING_SEASON_NAME].reindex(
                    total_heating_including_hotwater.index
                )
            ].index.month,
        }
    )

    # Calculate daily hot water energy consumption
    daily_hot_water_energy_consumption = (
        non_heating_season_consumption
        * (
            hourly_hot_water_month_profile[WEIGHT_NAME_REQUIRED]
            * (temperature_hot_water - induced_factors["cold_water_temperature"])
        )
        .resample("D")
        .transform("sum")
        / (
            hourly_hot_water_month_profile[WEIGHT_NAME_REQUIRED]
            * (temperature_hot_water - induced_factors["cold_water_temperature"])
        )[~induced_factors["closed_heating_season"]].sum()
    ).rename(ENERGY_FEATURE_NAME)

    for _, row in df.iterrows():
        mask_daily_hot_water_energy_consumption = (
            pd.DatetimeIndex(daily_hot_water_energy_consumption.index).to_period("M")
            == f"{row.Year}-{row.Month:02d}"
        )
        mask_total_heating_including_hotwater = (
            pd.DatetimeIndex(total_heating_including_hotwater.index).to_period("M")
            == f"{row.Year}-{row.Month:02d}"
        )
        daily_hot_water_energy_consumption.loc[mask_daily_hot_water_energy_consumption] = (
            total_heating_including_hotwater.loc[mask_total_heating_including_hotwater].iloc[0]
            * (
                hourly_hot_water_month_profile["weight"]
                * (temperature_hot_water - induced_factors["cold_water_temperature"])
            )
            .resample("D")
            .transform("sum")
            / (
                hourly_hot_water_month_profile["weight"]
                * (temperature_hot_water - induced_factors["cold_water_temperature"])
            )[mask_daily_hot_water_energy_consumption].sum()
        ).rename(ENERGY_FEATURE_NAME)

    # Calculate final hourly hot water energy consumption
    final_hourly_hot_water_energy_consumption = pd.DataFrame(
        (daily_hot_water_energy_consumption * hourly_hot_water_day_profil).rename(
            ENERGY_FEATURE_NAME
        )
    )

    # Return the result as HourlyHeatDemand
    return HourlyHeatDemand(name, final_hourly_hot_water_energy_consumption)
