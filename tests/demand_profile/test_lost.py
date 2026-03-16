import numpy as np
import pandas as pd
import pytest

from heatpro.demand_profile.building_heating_profile import WEIGHT_NAME_REQUIRED
from heatpro.demand_profile.loss_profile import (
    Y_to_H_thermal_loss_profile,
    InducedFactors,
)


# Fixture for a sample temperatures DataFrame
@pytest.fixture
def sample_temperatures():
    dates = pd.date_range("2022-01-01", periods=365, freq="D")
    return InducedFactors(
        supply_temperature=pd.Series(
            np.random.uniform(10, 20, 365), index=dates, name="supply_temperature"
        ),
        return_temperature=pd.Series(
            np.random.uniform(10, 20, 365), index=dates, name="return_temperature"
        ),
        soil_temperature=pd.Series(
            np.random.uniform(10, 20, 365), index=dates, name="soil_temperature"
        ),
    )


# Test Y_to_H_thermal_loss_profile
def test_Y_to_H_thermal_loss_profile(sample_temperatures):
    # Valid case
    thermal_loss_profile = Y_to_H_thermal_loss_profile(sample_temperatures)
    assert WEIGHT_NAME_REQUIRED in thermal_loss_profile.columns
    assert len(thermal_loss_profile) == len(
        sample_temperatures.supply_temperature.resample("h").sum()
    )
