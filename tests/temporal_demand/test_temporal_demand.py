import pandas as pd
import pytest
from matplotlib.axes import Axes
from heatpro.temporal_demand.temporal_heat_demand import TemporalHeatDemand
from heatpro.check import ENERGY_FEATURE_NAME

# Sample data for testing
sample_data = pd.DataFrame({
                            ENERGY_FEATURE_NAME: [100, 150, 120, 180, 200],
                            },
                           index=pd.date_range('2022-01-01', periods=5, freq='D'))

def test_temporal_heat_demand_creation():
    temporal_heat_demand = TemporalHeatDemand('SampleDemand', sample_data)

    assert temporal_heat_demand.name == 'SampleDemand'
    assert temporal_heat_demand.data.equals(sample_data)

def test_temporal_heat_demand_invalid_datetime_index():
    invalid_data = sample_data.copy()
    invalid_data.index = ['invalid', 'date', 'format', 'here', 'too']
    
    with pytest.raises(ValueError, match="data index should be in datetime format"):
        TemporalHeatDemand('InvalidDemand', invalid_data)

# def test_temporal_heat_demand_missing_energy_feature():
#     data_missing_energy = sample_data.rename({ENERGY_FEATURE_NAME:'erreur'},axis=1)  # Missing 'energy_demand' column
    
#     with pytest.raises(ValueError, match=f"data has no {ENERGY_FEATURE_NAME} (required)"):
#         TemporalHeatDemand('MissingEnergyDemand', data_missing_energy)

def test_temporal_heat_demand_plot():
    temporal_heat_demand = TemporalHeatDemand('SampleDemand', sample_data)
    plot_axes = temporal_heat_demand.plot()

    assert isinstance(plot_axes, Axes)
    # Add more specific assertions related to the plot if needed
