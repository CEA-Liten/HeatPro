from datetime import datetime

import pandas as pd

from ..check import find_duplicate_months, find_xor_months, ENERGY_FEATURE_NAME
from ..check import check_weight_format, WEIGHT_NAME_REQUIRED

from ..temporal_demand import YearlyHeatDemand, MonthlyHeatDemand, DailyHeatDemand, HourlyHeatDemand

def monthly_weighted_disaggregate(yearly_demand: YearlyHeatDemand, weights: pd.DataFrame,
                                  keep_year_data: bool = True) -> MonthlyHeatDemand:
    """Disaggregate yearly heat demand into monthly values using weights.

    Args:
        yearly_demand (YearlyHeatDemand): The input yearly heat demand to be disaggregated.
        weights (pd.DataFrame): DataFrame containing weights for each month.
        keep_year_data (bool, optional): If True, include yearly data in the output.
            Defaults to True.

    Raises:
        ValueError: If yearly_demand is not an instance of YearlyHeatDemand.
        ValueError: If the weight format is not valid.
        ValueError: If there are duplicate months in the weights index.
        ValueError: If yearly_demand and weights do not overlap on the same year.

    Returns:
        MonthlyHeatDemand: The disaggregated monthly heat demand.
    """
    # Check if yearly_demand is an instance of YearlyHeatDemand
    if not isinstance(yearly_demand, YearlyHeatDemand):
        raise ValueError("yearly_demand should be an instance of YearlyHeatDemand")

    # Check the format of the weights DataFrame
    check_weight_format(weights)

    # Check for duplicate months in the weights index
    duplicate_months = find_duplicate_months(weights.index)
    if not duplicate_months.empty:
        duplicate_month_str = ', '.join([f'{month.Month}-{month.Year}' for _, month in duplicate_months.iterrows()])
        raise ValueError(f"Months {duplicate_month_str} have multiple occurrences in weights")

    # Check if yearly_demand and weights overlap on the same year
    if not yearly_demand.data.index.year.equals(weights.index.year.unique()):
        raise ValueError("yearly_demand and weights do not overlap on the same year")

    # Initialize the DataFrame for monthly demand
    monthly_demand_df = weights.copy()

    # Include yearly data in the output if keep_year_data is True
    if keep_year_data:
        for feature in yearly_demand.data.columns:
            monthly_demand_df[f"yearly_{feature}"] = sum(
                (weights.index.year == index.year) * row[feature]
                for index, row in yearly_demand.data.iterrows()
            )

    # Disaggregate the yearly heat demand into monthly values
    monthly_demand_df[ENERGY_FEATURE_NAME] = sum(
        (weights.index.year == index.year) * row[ENERGY_FEATURE_NAME] *
        weights[WEIGHT_NAME_REQUIRED]
        for index, row in yearly_demand.data.iterrows()
    )

    # Create a MonthlyHeatDemand object with the disaggregated data
    return MonthlyHeatDemand(yearly_demand.name, monthly_demand_df)

def weekly_weighted_disaggregate(monthly_demand: MonthlyHeatDemand, weights: pd.DataFrame,
                                 keep_year_data: bool = True) -> HourlyHeatDemand:
    """Disaggregate monthly heat demand into hourly values using weights.

    Args:
        monthly_demand (MonthlyHeatDemand): The input monthly heat demand to be disaggregated.
        weights (pd.DataFrame): DataFrame containing weights for each week.
        keep_year_data (bool, optional): If True, include yearly data in the output.
            Defaults to True.

    Raises:
        ValueError: If monthly_demand is not an instance of MonthlyHeatDemand.
        ValueError: If the weight format is not valid.
        ValueError: If weights and monthly_demand do not match the same months.

    Returns:
        HourlyHeatDemand: The disaggregated hourly heat demand.
    """
    # Check if monthly_demand is an instance of MonthlyHeatDemand
    if not isinstance(monthly_demand, MonthlyHeatDemand):
        raise ValueError("monthly_demand should be an instance of MonthlyHeatDemand")

    # Check the format of the weights DataFrame
    check_weight_format(weights)

    # Check if weights and monthly_demand match the same months
    xor_months = find_xor_months(monthly_demand.data, weights)
    if not xor_months.empty:
        diff_str = f"weights and monthly_demand are not matching the same month\n Difference :\n {xor_months}"
        raise ValueError(diff_str)

    # Initialize the DataFrame for hourly demand
    hourly_demand_df = weights.copy()

    # Include yearly data in the output if keep_year_data is True
    if keep_year_data:
        for feature in monthly_demand.data.columns:
            if not feature.startswith('yearly_'):
                hourly_demand_df[f'monthly_{feature}'] = sum(
                    (weights.index.year == index.year) *
                    (weights.index.month == index.month) *
                    row[feature]
                    for index, row in monthly_demand.data.iterrows()
                )
            else:
                hourly_demand_df[feature] = sum(
                    (weights.index.year == index.year) *
                    (weights.index.month == index.month) *
                    row[feature]
                    for index, row in monthly_demand.data.iterrows()
                )

    # Disaggregate the monthly heat demand into hourly values
    hourly_demand_df[ENERGY_FEATURE_NAME] = sum(
        (weights.index.year == index.year) *
        (weights.index.month == index.month) *
        row[ENERGY_FEATURE_NAME] *
        weights[WEIGHT_NAME_REQUIRED]
        for index, row in monthly_demand.data.iterrows()
    )

    # Create an HourlyHeatDemand object with the disaggregated data
    return HourlyHeatDemand(monthly_demand.name, hourly_demand_df)
 
def daily_weighted_dissagregate(monthly_demand: MonthlyHeatDemand, weights: pd.DataFrame,
                                keep_month_data: bool = True) -> DailyHeatDemand:
    """Disaggregate monthly heat demand into daily values using weights.

    Args:
        monthly_demand (MonthlyHeatDemand): The input monthly heat demand to be disaggregated.
        weights (pd.DataFrame): DataFrame containing weights for each day.
        keep_month_data (bool, optional): If True, include monthly data in the output.
            Defaults to True.

    Raises:
        ValueError: If monthly_demand is not an instance of MonthlyHeatDemand.
        ValueError: If the weight format is not valid.
        ValueError: If weights and monthly_demand do not match the same months.

    Returns:
        DailyHeatDemand: The disaggregated daily heat demand.
    """
    # Check if monthly_demand is an instance of MonthlyHeatDemand
    if not isinstance(monthly_demand, MonthlyHeatDemand):
        raise ValueError("monthly_demand should be an instance of MonthlyHeatDemand")

    # Check the format of the weights DataFrame
    check_weight_format(weights)

    # Check if weights and monthly_demand match the same months
    xor_months = find_xor_months(monthly_demand.data, weights)
    if not xor_months.empty:
        diff_str = f"weights and monthly_demand are not matching the same month\n Difference :\n {xor_months}"
        raise ValueError(diff_str)

    # Initialize the DataFrame for daily demand
    daily_demand_df = weights.copy()

    # Include monthly data in the output if keep_month_data is True
    if keep_month_data:
        for feature in monthly_demand.data.columns:
            if not feature.startswith('yearly_'):
                daily_demand_df[f'monthly_{feature}'] = sum(
                    (weights.index.year == index.year) *
                    (weights.index.month == index.month) *
                    row[feature]
                    for index, row in monthly_demand.data.iterrows()
                )
            else:
                daily_demand_df[feature] = sum(
                    (weights.index.year == index.year) *
                    (weights.index.month == index.month) *
                    row[feature]
                    for index, row in monthly_demand.data.iterrows()
                )

    # Disaggregate the monthly heat demand into daily values
    daily_demand_df[ENERGY_FEATURE_NAME] = sum(
        (weights.index.year == index.year) *
        (weights.index.month == index.month) *
        row[ENERGY_FEATURE_NAME] *
        weights[WEIGHT_NAME_REQUIRED]
        for index, row in monthly_demand.data.iterrows()
    )

    # Create a DailyHeatDemand object with the disaggregated data
    return DailyHeatDemand(monthly_demand.name, daily_demand_df)

def hourly_weighted_dissagregate(daily_demand: DailyHeatDemand, weights: pd.DataFrame,
                                keep_month_data: bool = True) -> HourlyHeatDemand:
    """Disaggregate daily heat demand into hourly values using weights.

    Args:
        daily_demand (DailyHeatDemand): The input daily heat demand to be disaggregated.
        weights (pd.DataFrame): DataFrame containing weights for each hour.
        keep_month_data (bool, optional): If True, include monthly data in the output.
            Defaults to True.

    Raises:
        ValueError: If daily_demand is not an instance of DailyHeatDemand.
        ValueError: If the weight format is not valid.
        ValueError: If weights and daily_demand do not match the same months.

    Returns:
        HourlyHeatDemand: The disaggregated hourly heat demand.
    """
    # Check if daily_demand is an instance of DailyHeatDemand
    if not isinstance(daily_demand, DailyHeatDemand):
        raise ValueError("daily_demand should be an instance of DailyHeatDemand")

    # Check the format of the weights DataFrame
    check_weight_format(weights)

    # Check if weights and daily_demand match the same months
    xor_months = find_xor_months(daily_demand.data, weights)
    if not xor_months.empty:
        diff_str = f"weights and daily_demand are not matching the same month\n Difference :\n {xor_months}"
        raise ValueError(diff_str)

    # Initialize the DataFrame for hourly demand
    hourly_demand_df = weights.copy()

    # Include monthly data in the output if keep_month_data is True
    if keep_month_data:
        for feature in daily_demand.data.columns:
            if not (feature.startswith('yearly_') or feature.startswith('monthly_')):
                hourly_demand_df[f'daily_{feature}'] = sum(
                    (weights.index.year == index.year) *
                    (weights.index.month == index.month) *
                    row[feature]
                    for index, row in daily_demand.data.iterrows()
                )
            else:
                hourly_demand_df[feature] = sum(
                    (weights.index.year == index.year) *
                    (weights.index.month == index.month) *
                    row[feature]
                    for index, row in daily_demand.data.iterrows()
                )

    # Disaggregate the daily heat demand into hourly values
    hourly_demand_df[ENERGY_FEATURE_NAME] = sum(
        (weights.index.year == index.year) *
        (weights.index.month == index.month) *
        row[ENERGY_FEATURE_NAME] *
        weights[WEIGHT_NAME_REQUIRED]
        for index, row in daily_demand.data.iterrows()
    )

    # Create an HourlyHeatDemand object with the disaggregated data
    return HourlyHeatDemand(daily_demand.name, hourly_demand_df)

    
    
    
    
    




 
    