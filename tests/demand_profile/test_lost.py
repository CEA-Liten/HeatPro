import numpy as np
import pandas as pd
import pytest
from heatpro.demand_profile.loss_profile import Y_to_H_thermal_loss_profile, WEIGHT_NAME_REQUIRED, DEPARTURE_TEMPERATURE_NAME, RETURN_TEMPERATURE_NAME, SOIL_TEMPERATURE_NAME

# Fixture for a sample temperatures DataFrame
@pytest.fixture
def sample_temperatures():
    dates = pd.date_range('2022-01-01', periods=365, freq='D')
    data = {
        DEPARTURE_TEMPERATURE_NAME: np.random.uniform(10, 20, 365),
        RETURN_TEMPERATURE_NAME: np.random.uniform(5, 15, 365),
        SOIL_TEMPERATURE_NAME: np.random.uniform(0, 10, 365)
    }
    df = pd.DataFrame(data, index=dates)
    return df

# Test Y_to_H_thermal_loss_profile
def test_Y_to_H_thermal_loss_profile(sample_temperatures):
    # Valid case
    thermal_loss_profile = Y_to_H_thermal_loss_profile(sample_temperatures)
    assert WEIGHT_NAME_REQUIRED in thermal_loss_profile.columns
    assert len(thermal_loss_profile) == len(sample_temperatures.resample('h').sum())

    # Additional tests for edge cases or specific scenarios.
