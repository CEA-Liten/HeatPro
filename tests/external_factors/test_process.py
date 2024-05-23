import pandas as pd
import pytest
from heatpro.external_factors import convert_serie_C_to_F, convert_serie_F_to_C, get_coldest_dayofyear, ExternalFactors

# Sample data for testing
sample_data = pd.DataFrame({
    'external_temperature': [10.0, 15.0, 20.0],
    'heating_season':[True,False,True],
}, index=pd.date_range('2022-01-01', periods=3, freq='D'))

def test_convert_serie_C_to_F():
    celsius_series = sample_data['external_temperature']
    expected_result = pd.Series([50.0, 59.0, 68.0], index=celsius_series.index)
    
    result = convert_serie_C_to_F(celsius_series)
    
    assert result.equals(expected_result)

def test_convert_serie_F_to_C():
    fahrenheit_series = convert_serie_C_to_F(sample_data['external_temperature'])
    expected_result = sample_data['external_temperature']
    
    result = convert_serie_F_to_C(fahrenheit_series)
    
    assert result.equals(expected_result)

def test_get_coldest_dayofyear():
    external_factors = ExternalFactors(sample_data)
    coldest_day_of_year = get_coldest_dayofyear(external_factors)
    
    assert coldest_day_of_year == 1  # Assuming data starts from the first day of the year

# # Additional test for invalid input
# def test_convert_serie_C_to_F_invalid_input():
#     with pytest.raises(TypeError, match="Expected input of type pd.Series"):
#         convert_serie_C_to_F([10.0, 15.0, 20.0])

# # Additional test for invalid input
# def test_convert_serie_F_to_C_invalid_input():
#     with pytest.raises(TypeError, match="Expected input of type pd.Series"):
#         convert_serie_F_to_C([50.0, 59.0, 68.0])
