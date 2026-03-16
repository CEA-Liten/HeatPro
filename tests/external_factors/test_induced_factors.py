import pytest
import pandas as pd
from heatpro.external_factors.induced_factors import InducedFactors


def test_induced_factors_initialization():
    # Test with all fields None
    factors = InducedFactors()
    assert factors.supply_temperature is None
    assert factors.return_temperature is None
    assert factors.soil_temperature is None
    assert factors.closed_heating_season is None
    assert factors.cold_water_temperature is None

    # Test with some fields populated
    index = pd.date_range("2023-01-01", periods=3)
    supply_temp = pd.Series([20, 21, 22], index=index)
    return_temp = pd.Series([15, 16, 17], index=index)
    factors = InducedFactors(supply_temperature=supply_temp, return_temperature=return_temp)
    assert factors.supply_temperature.equals(supply_temp)
    assert factors.return_temperature.equals(return_temp)


def test_induced_factors_index_mismatch():
    # Create series with different indexes
    index1 = pd.date_range("2023-01-01", periods=3)
    index2 = pd.date_range("2023-01-02", periods=3)
    supply_temp = pd.Series([20, 21, 22], index=index1)
    return_temp = pd.Series([15, 16, 17], index=index2)

    # Test that ValueError is raised when indexes don't match
    with pytest.raises(
        ValueError,
        match="Index mismatch: 'return_temperature' series index does not match 'supply_temperature' series index",
    ):
        InducedFactors(supply_temperature=supply_temp, return_temperature=return_temp)


def test_induced_factors_single_series():
    # Test that initialization with a single series doesn't raise an error
    index = pd.date_range("2023-01-01", periods=3)
    supply_temp = pd.Series([20, 21, 22], index=index)
    factors = InducedFactors(supply_temperature=supply_temp)
    assert factors.supply_temperature.equals(supply_temp)
    assert factors.return_temperature is None
    assert factors.soil_temperature is None
    assert factors.closed_heating_season is None
    assert factors.cold_water_temperature is None
