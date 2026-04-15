import pandas as pd

SET_TEMPERATURE_COLD = 22


def year_to_hour_outdoor_temperarure_distribution(
    yearly_power_cold_demand: pd.Series,
    felt_temperature: pd.Series,
    weigths: pd.Series = None,
    set_temperature: float = SET_TEMPERATURE_COLD,
) -> pd.Series:
    if weigths is None:
        weigths = pd.Series(1, index=felt_temperature.index)
    if not weigths.index.equals(felt_temperature.index):
        raise ValueError("weigths and felt_temperature must have identical index")
    yearly_power_cold_demand_reindex = yearly_power_cold_demand.reindex(
        felt_temperature.index, method="ffill"
    )
    return (
        yearly_power_cold_demand_reindex
        * ((felt_temperature - set_temperature).clip(0) * weigths)
        / ((felt_temperature - set_temperature).clip(0) * weigths).resample("YS").transform("mean")
    ).rename(yearly_power_cold_demand_reindex.name)


def month_to_hour_outdoor_temperarure_distribution(
    monthly_power_cold_demand: pd.Series,
    felt_temperature: pd.Series,
    weigths: pd.Series = None,
    set_temperature: float = SET_TEMPERATURE_COLD,
) -> pd.Series:
    if weigths is None:
        weigths = pd.Series(1, index=felt_temperature.index)
    if not weigths.index.equals(felt_temperature.index):
        raise ValueError("weigths and felt_temperature must have identical index")
    monthly_power_cold_demand_reindex = monthly_power_cold_demand.reindex(
        felt_temperature.index, method="ffill"
    )
    return (
        monthly_power_cold_demand_reindex
        * ((felt_temperature - set_temperature).clip(0) * weigths)
        / ((felt_temperature - set_temperature).clip(0) * weigths).resample("MS").transform("mean")
    ).rename(monthly_power_cold_demand_reindex.name)
