import pandas as pd
import numpy as np
import pytest
from heatpro.demand_profile.hot_water_profile import (WEIGHT_NAME_REQUIRED, COLD_WATER_TEMPERATURE_NAME,
                         basic_hot_water_monthly_profile, basic_hot_water_hourly_profile)

# Fixture for a sample cold_water_temperature DataFrame
@pytest.fixture
def sample_cold_water_temperature():
    return pd.DataFrame({COLD_WATER_TEMPERATURE_NAME: np.random.uniform(5, 15, 365)},
                        index=pd.date_range('2022-01-01', periods=365, freq='D'))

# Fixture for a sample monthly_HW_weight DataFrame
@pytest.fixture
def sample_monthly_HW_weight():
    return pd.DataFrame({WEIGHT_NAME_REQUIRED: np.random.uniform(0.1, 1, 12)},
                        index=pd.date_range('2022-01-01', periods=12, freq='MS'))

# Fixture for a sample raw_hourly_hotwater_profile DataFrame
@pytest.fixture
def sample_raw_hourly_hotwater_profile():
    return pd.DataFrame({WEIGHT_NAME_REQUIRED: np.random.uniform(0.1, 1, 24*365)},
                        index=pd.date_range('2022-01-01', periods=24*365, freq='h'))

# Test basic_hot_water_monthly_profile
def test_basic_hot_water_monthly_profile(sample_cold_water_temperature, sample_monthly_HW_weight):
    # Valid case
    monthly_hot_water_profile = basic_hot_water_monthly_profile(sample_cold_water_temperature, 70, sample_monthly_HW_weight)
    assert WEIGHT_NAME_REQUIRED in monthly_hot_water_profile.columns
    assert len(monthly_hot_water_profile) == len(sample_monthly_HW_weight)

    # Invalid case with mismatched months
    invalid_monthly_HW_weight = sample_monthly_HW_weight.copy()
    invalid_monthly_HW_weight.index = invalid_monthly_HW_weight.index + pd.DateOffset(months=1)
    with pytest.raises(ValueError, match="cold_water_temperature and monthly_HW_weight index do not match"):
        basic_hot_water_monthly_profile(sample_cold_water_temperature, 70, invalid_monthly_HW_weight)

    # Additional tests for edge cases or specific scenarios.

# Test basic_hot_water_hourly_profile
def test_basic_hot_water_hourly_profile(sample_raw_hourly_hotwater_profile):
    # Valid case
    hourly_hotwater_profile = basic_hot_water_hourly_profile(sample_raw_hourly_hotwater_profile, 0.8, 0.9)
    assert WEIGHT_NAME_REQUIRED in hourly_hotwater_profile.columns
    assert len(hourly_hotwater_profile) == len(sample_raw_hourly_hotwater_profile)

    # Additional tests for edge cases or specific scenarios.
