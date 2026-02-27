import pandas as pd
import plotly.graph_objects as go
import pytest
from heatpro.external_factors import ExternalFactors

# Sample data for testing
sample_data = pd.DataFrame({
                            'external_temperature': [10.0, 15.0, 20.0],
                            'heating_season': [1, 0, 1],
                            },
                           index=pd.to_datetime(['2021-01','2021-02','2021-03']))

def test_external_factors():
    # Test if ExternalFactors initializes correctly with valid data
    external_factors = ExternalFactors(
        sample_data["external_temperature"],
        sample_data["heating_season"],
    )
    
    assert external_factors.temperature.equals(sample_data["external_temperature"])
    assert external_factors.heating_season.equals(sample_data["heating_season"])

def test_external_factors_indexes_not_matching():
    # Test if ExternalFactors raises an error for missing features
    temperature = pd.Series({'external_temperature': [1, 2, 3]},index=pd.to_datetime(['2021-01','2021-02','2021-03']))
    heating_season = pd.Series({'heating_season': [1, 2, 3]},index=pd.to_datetime(['2022-01','2022-02','2022-03']))
    
    with pytest.raises(ValueError, match="temperature and heating_season must have same index"):
        ExternalFactors(temperature,heating_season)

def test_external_factors_invalid_index():
    # Test if ExternalFactors raises an error for an invalid index
    temperature = pd.Series({'external_temperature': [1, 2, 3]},index=['2021-01','2021-02','2021-03'])
    heating_season = pd.Series({'heating_season': [1, 2, 3]},index=['2022-01','2022-02','2022-03'])
    
    with pytest.raises(ValueError, match="temperature index must be a DatetimeIndex"):
        ExternalFactors(temperature,heating_season)

def test_external_factors_plot():
    # Test if plot function returns Axes object
    external_factors = ExternalFactors(
        sample_data["external_temperature"],
        sample_data["heating_season"],
    )
    
    plot_axes = external_factors.plot()
    
    assert isinstance(plot_axes, go.Figure)
