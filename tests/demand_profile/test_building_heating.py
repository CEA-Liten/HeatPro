import pandas as pd
import numpy as np
import pytest

from heatpro.check.check_weight_format import WEIGHT_NAME_REQUIRED
from heatpro.demand_profile.building_heating_profile import basic_building_heating_profile

# Fixture for a sample felt_temperature DataFrame
@pytest.fixture
def sample_felt_temperature():
    return pd.DataFrame({'felt_temperature': np.random.uniform(10, 20, 24)},
                        index=pd.date_range('2022-01-01', periods=24, freq='h'))

# Fixture for a sample hourly_weight DataFrame
@pytest.fixture
def sample_hourly_weight():
    X = np.random.uniform(0.1, 1, 24)
    X = X/X.sum()
    return pd.DataFrame({'weight': X},
                        index=pd.date_range('2022-01-01', periods=24, freq='h'))

# Test basic_building_heating_profile
def test_basic_building_heating_profile(sample_felt_temperature, sample_hourly_weight):
    # Valid case
    building_heating_profile = basic_building_heating_profile(sample_felt_temperature, 15, sample_hourly_weight)
    assert WEIGHT_NAME_REQUIRED in building_heating_profile.columns
    assert len(building_heating_profile) == len(sample_hourly_weight)

    # Invalid case with mismatched hours
    invalid_felt_temperature = sample_felt_temperature.copy()
    invalid_felt_temperature.index = invalid_felt_temperature.index + pd.DateOffset(hours=1)
    with pytest.raises(ValueError, match="felt_temperature and hourly_weight hours are not match"):
        basic_building_heating_profile(invalid_felt_temperature, 15, sample_hourly_weight)

    # Additional tests for edge cases or specific scenarios.
