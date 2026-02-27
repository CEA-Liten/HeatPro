import pandas as pd
import pytest
from heatpro.external_factors import basic_temperature_departure, ExternalFactors, DEPARTURE_TEMPERATURE_NAME

# Sample data for testing
sample_data = pd.DataFrame({
    'external_temperature': [10.0, 15.0, 20.0, 25.0, 30.0],
    'heating_season': [0, 1, 1, 0, 0],
}, index=pd.date_range('2022-01-01', periods=5, freq='D'))

def test_basic_temperature_departure():
    external_factors = ExternalFactors(
        temperature=sample_data["external_temperature"],
        heating_season=sample_data["heating_season"]
    )
    T_max_HS, T_max_NHS, T_min_HS, T_min_NHS, T_ext_mid, T_ext_min = 30, 20, 10, 5, 25, 15
    result = basic_temperature_departure(external_factors, T_max_HS, T_max_NHS, T_min_HS, T_min_NHS, T_ext_mid, T_ext_min)

    assert isinstance(result, pd.DataFrame)
    assert DEPARTURE_TEMPERATURE_NAME in result.columns
    assert result.index.equals(sample_data.index)
