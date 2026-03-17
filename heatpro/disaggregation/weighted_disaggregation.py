import pandas as pd

from ..check import find_duplicate_months, find_xor_months, ENERGY_FEATURE_NAME

from ..temporal_demand import HourlyHeatDemand


def monthly_weighted_disaggregate(
    yearly_demand: pd.Series,
    weights: pd.Series,
) -> pd.Series:
    """Disaggregate yearly heat demand into monthly values using weights.

    Args:
        yearly_demand (pd.Series): The input yearly heat demand to be disaggregated.
        weights (pd.Series): Series containing weights for each month.
        keep_year_data (bool, optional): If True, include yearly data in the output.
            Defaults to True.

    Raises:
        ValueError: If the weight format is not valid.
        ValueError: If there are duplicate months in the weights index.
        ValueError: If yearly_demand and weights do not overlap on the same year.

    Returns:
        pd.Series: The disaggregated monthly heat demand.
    """
    # Check for duplicate months in the weights index
    duplicate_months = find_duplicate_months(weights.index)
    if not duplicate_months.empty:
        duplicate_month_str = ", ".join(
            [f"{month.Month}-{month.Year}" for _, month in duplicate_months.iterrows()]
        )
        raise ValueError(f"Months {duplicate_month_str} have multiple occurrences in weights")

    # Check if yearly_demand and weights overlap on the same year
    if not yearly_demand.index.year.equals(weights.index.year.unique()):
        raise ValueError("yearly_demand and weights do not overlap on the same year")

    # Disaggregate the yearly heat demand into monthly values
    monthly_demand = yearly_demand.reindex(weights.index).ffill() * weights

    return monthly_demand


def weekly_weighted_disaggregate(
    monthly_demand: pd.Series, weights: pd.Series, keep_year_data: bool = True
) -> HourlyHeatDemand:
    """Disaggregate monthly heat demand into hourly values using weights.

    Args:
        monthly_demand (pd.Series): The input monthly heat demand to be disaggregated.
        weights (pd.DataFrame): DataFrame containing weights for each week.
        keep_year_data (bool, optional): If True, include yearly data in the output.
            Defaults to True.

    Raises:
        ValueError: If the weight format is not valid.
        ValueError: If weights and monthly_demand do not match the same months.

    Returns:
        HourlyHeatDemand: The disaggregated hourly heat demand.
    """
    # Check if weights and monthly_demand match the same months
    xor_months = find_xor_months(monthly_demand, weights)
    if not xor_months.empty:
        diff_str = f"weights and monthly_demand are not matching the same month\n Difference :\n {xor_months}"
        raise ValueError(diff_str)

    # Initialize the DataFrame for hourly demand
    hourly_demand_df = weights.copy().to_frame()

    # Disaggregate the monthly heat demand into hourly values
    hourly_demand_df[ENERGY_FEATURE_NAME] = sum(
        (weights.index.year == index.year) * (weights.index.month == index.month) * value * weights
        for index, value in monthly_demand.items()
    )

    # Create an HourlyHeatDemand object with the disaggregated data
    return HourlyHeatDemand(monthly_demand.name, hourly_demand_df)


