import pandas as pd
from matplotlib.axes import Axes
import pytest
from heatpro.external_factors import ExternalFactors, EXTERNAL_TEMPERATURE_NAME

# Sample data for testing
sample_data = pd.DataFrame({
                            'external_temperature': [10.0, 15.0, 20.0],
                            'heating_season': [1, 0, 1],
                            },
                           index=pd.to_datetime(['2021-01','2021-02','2021-03']))

def test_external_factors():
    # Test if ExternalFactors initializes correctly with valid data
    external_factors = ExternalFactors(sample_data)
    
    assert external_factors.data.equals(sample_data)

def test_external_factors_missing_features():
    # Test if ExternalFactors raises an error for missing features
    invalid_data = pd.DataFrame({'invalid_feature': [1, 2, 3]})
    
    with pytest.raises(ValueError, match="Missing required features"):
        ExternalFactors(invalid_data)

def test_external_factors_invalid_index():
    # Test if ExternalFactors raises an error for an invalid index
    invalid_index_data = pd.DataFrame({'external_temperature': [1, 2, 3],'heating_season': [1, 0, 1],}, index=['2022-01-01', '2022-01-02', '2022-01-03'])
    
    with pytest.raises(ValueError, match="data_external_factors index should be in datetime format"):
        ExternalFactors(invalid_index_data)

def test_external_factors_plot():
    # Test if plot function returns Axes object
    external_factors = ExternalFactors(sample_data)
    
    plot_axes = external_factors.plot()
    
    assert isinstance(plot_axes, Axes)
