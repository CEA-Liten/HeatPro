import pandas as pd

SET_TEMPERATURE_COLD = 22


def year_to_hour_outdoor_temperarure_distribution(
    yearly_power_cold_demand: pd.Series,
    felt_temperature: pd.Series,
    weigths: pd.Series = None,
    set_temperature: float = SET_TEMPERATURE_COLD,
) -> pd.Series:
    """Disaggregate yearly cold demand to hourly values based on outdoor temperature.

    This function takes yearly cold demand data and distributes it hourly based on outdoor
    temperature, considering a set temperature threshold. It accounts for temperature
    differences above the set threshold and applies optional weights.

    Args:
        yearly_power_cold_demand (pd.Series): Yearly cold demand values with datetime index.
        felt_temperature (pd.Series): Outdoor temperature values with datetime index.
        weigths (pd.Series, optional): Optional weights for temperature adjustment.
            Defaults to None (equal weights).
        set_temperature (float, optional): Temperature threshold below which no cold demand
            is considered. Defaults to SET_TEMPERATURE_COLD (22°C).

    Raises:
        ValueError: If weights and felt_temperature have different indices.

    Returns:
        pd.Series: Hourly disaggregated cold demand with datetime index.
    """
    if weigths is None:
        weigths = pd.Series(1, index=felt_temperature.index)
    if not weigths.index.equals(felt_temperature.index):
        raise ValueError("weigths and felt_temperature must have identical index")
    yearly_power_cold_demand_reindex = yearly_power_cold_demand.reindex(
        felt_temperature.index, method="ffill"
    )
    return (
        (
            yearly_power_cold_demand_reindex
            * ((felt_temperature - set_temperature).clip(0) * weigths)
            / ((felt_temperature - set_temperature).clip(0) * weigths)
            .resample("YS")
            .transform("mean")
        )
        .fillna(0.0)
        .rename(yearly_power_cold_demand_reindex.name)
    )


def month_to_hour_outdoor_temperarure_distribution(
    monthly_power_cold_demand: pd.Series,
    felt_temperature: pd.Series,
    weigths: pd.Series = None,
    set_temperature: float = SET_TEMPERATURE_COLD,
) -> pd.Series:
    """Disaggregate monthly cold demand to hourly values based on outdoor temperature.

    This function takes monthly cold demand data and distributes it hourly based on outdoor
    temperature, considering a set temperature threshold. It accounts for temperature
    differences above the set threshold and applies optional weights.

    Args:
        monthly_power_cold_demand (pd.Series): Monthly cold demand values with datetime index.
        felt_temperature (pd.Series): Outdoor temperature values with datetime index.
        weigths (pd.Series, optional): Optional weights for temperature adjustment.
            Defaults to None (equal weights).
        set_temperature (float, optional): Temperature threshold below which no cold demand
            is considered. Defaults to SET_TEMPERATURE_COLD (22°C).

    Raises:
        ValueError: If weights and felt_temperature have different indices.

    Returns:
        pd.Series: Hourly disaggregated cold demand with datetime index.
    """
    if weigths is None:
        weigths = pd.Series(1, index=felt_temperature.index)
    if not weigths.index.equals(felt_temperature.index):
        raise ValueError("weigths and felt_temperature must have identical index")
    monthly_power_cold_demand_reindex = monthly_power_cold_demand.reindex(
        felt_temperature.index, method="ffill"
    )
    return (
        (
            monthly_power_cold_demand_reindex
            * ((felt_temperature - set_temperature).clip(0) * weigths)
            / ((felt_temperature - set_temperature).clip(0) * weigths)
            .resample("MS")
            .transform("mean")
        )
        .fillna(0.0)
        .rename(monthly_power_cold_demand_reindex.name)
    )
