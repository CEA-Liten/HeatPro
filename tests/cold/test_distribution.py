# tests/test_distribution.py
import pandas as pd
import pytest
from heatpro.cold.distribution import (
    year_to_hour_outdoor_temperarure_distribution,
    month_to_hour_outdoor_temperarure_distribution,
    SET_TEMPERATURE_COLD,
)


# Create test data
def create_test_data():
    date_range = pd.date_range("2023-01-01", "2023-12-31", periods=6)

    felt_temperature = pd.Series([0, 22, 30, 25, 30, 20], index=date_range, name="felt")
    weights = pd.Series([1.0] * len(date_range), index=date_range, name="felt")

    yearly_power_cold_demand = pd.Series(
        [1000.0] * len(date_range), index=date_range, name="yearly_power_cold_demand"
    )

    monthly_power_cold_demand = pd.Series(
        [100.0] * len(date_range), index=date_range, name="monthly_power_cold_demand"
    )

    return felt_temperature, weights, yearly_power_cold_demand, monthly_power_cold_demand


def test_year_to_hour_outdoor_temperarure_distribution():
    # Create test data
    felt_temperature, weights, yearly_power_cold_demand, _ = create_test_data()

    # Test with default set temperature
    result = year_to_hour_outdoor_temperarure_distribution(
        yearly_power_cold_demand, felt_temperature, weights
    )
    assert isinstance(result, pd.Series)
    assert result.name == "yearly_power_cold_demand"
    assert result.index.equals(yearly_power_cold_demand.index)
    assert result.iloc[0] == 0.0
    assert result.iloc[1] == 0.0
    assert result.iloc[2] == pytest.approx(
        (30 - SET_TEMPERATURE_COLD)
        / (
            (30 - SET_TEMPERATURE_COLD + 25 - SET_TEMPERATURE_COLD + 30 - SET_TEMPERATURE_COLD)
            / len(result)
        )
        * 1000.0,
        abs=1e-9,
    )

    # Test with custom set temperature
    result = year_to_hour_outdoor_temperarure_distribution(
        yearly_power_cold_demand, felt_temperature, weights, set_temperature=20.0
    )
    assert isinstance(result, pd.Series)
    assert result.name == "yearly_power_cold_demand"
    assert result.index.equals(yearly_power_cold_demand.index)

    # Test with None weights
    result = year_to_hour_outdoor_temperarure_distribution(
        yearly_power_cold_demand, felt_temperature
    )
    assert isinstance(result, pd.Series)
    assert result.name == "yearly_power_cold_demand"
    assert result.index.equals(yearly_power_cold_demand.index)


def test_year_to_hour_outdoor_temperarure_distribution_invalid_weights():
    # Create test data
    felt_temperature, weights, yearly_power_cold_demand, _ = create_test_data()

    # Test with invalid weights
    with pytest.raises(ValueError):
        year_to_hour_outdoor_temperarure_distribution(
            yearly_power_cold_demand, felt_temperature, weights[:-1]
        )


def test_month_to_hour_outdoor_temperarure_distribution():
    # Create test data
    felt_temperature, weights, _, monthly_power_cold_demand = create_test_data()

    # Test with default set temperature
    result = month_to_hour_outdoor_temperarure_distribution(
        monthly_power_cold_demand, felt_temperature, weights
    )
    assert isinstance(result, pd.Series)
    assert result.name == "monthly_power_cold_demand"
    assert result.index.equals(monthly_power_cold_demand.index)

    # Test with custom set temperature
    result = month_to_hour_outdoor_temperarure_distribution(
        monthly_power_cold_demand, felt_temperature, weights, set_temperature=20.0
    )
    assert isinstance(result, pd.Series)
    assert result.name == "monthly_power_cold_demand"
    assert result.index.equals(monthly_power_cold_demand.index)

    # Test with None weights
    result = month_to_hour_outdoor_temperarure_distribution(
        monthly_power_cold_demand, felt_temperature
    )
    assert isinstance(result, pd.Series)
    assert result.name == "monthly_power_cold_demand"
    assert result.index.equals(monthly_power_cold_demand.index)


def test_month_to_hour_outdoor_temperarure_distribution_invalid_weights():
    # Create test data
    felt_temperature, weights, _, monthly_power_cold_demand = create_test_data()

    # Test with invalid weights
    with pytest.raises(ValueError):
        month_to_hour_outdoor_temperarure_distribution(
            monthly_power_cold_demand, felt_temperature, weights[:-1]
        )
