import pandas as pd
import pytest
from heatpro.external_factors import basic_temperature_return, ExternalFactors, RETURN_TEMPERATURE_NAME

# Sample data for testing
sample_data = pd.DataFrame({
    'external_temperature': [10.0, 15.0, 20.0, 25.0, 30.0],
    'heating_season': [0, 1, 1, 0, 0],
}, index=pd.date_range('2022-01-01', periods=5, freq='D'))

def test_basic_temperature_return():
    external_factors = ExternalFactors(sample_data)
    T_HS, T_NHS = 30, 20
    result = basic_temperature_return(external_factors, T_HS, T_NHS)

    assert isinstance(result, pd.DataFrame)
    assert RETURN_TEMPERATURE_NAME in result.columns
    assert result.index.equals(sample_data.index)

    # Add more specific assertions based on your expectations

# Additional test for handling invalid input
def test_basic_temperature_return_invalid_input():
    invalid_factors = pd.DataFrame({'temperature': [10.0, 15.0, 20.0]}, index=pd.date_range('2022-01-01', periods=3, freq='D'))
    
    with pytest.raises(ValueError, match="Missing required features"):
        basic_temperature_return(ExternalFactors(invalid_factors), 30, 20)
