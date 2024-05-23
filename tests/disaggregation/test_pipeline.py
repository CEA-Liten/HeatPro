from functools import reduce
from typing import Callable
import pandas as pd
import pytest

from heatpro.disaggregation import compose, disaggregate_temporal_demand, TemporalHeatDemand
from heatpro.check import ENERGY_FEATURE_NAME

# Sample data for testing
class MockTemporalHeatDemand(TemporalHeatDemand):
    def __init__(self, data):
        super().__init__('mock', data)

# Mock functions for testing
def add_one_demand(demand: TemporalHeatDemand) -> TemporalHeatDemand:
    return MockTemporalHeatDemand(demand.data + 1)

def multiply_by_two_demand(demand: TemporalHeatDemand) -> TemporalHeatDemand:
    return MockTemporalHeatDemand(demand.data * 2)

def test_compose():
    # Test if compose correctly combines functions
    composed_function = compose([multiply_by_two_demand, add_one_demand])
    
    input_demand = MockTemporalHeatDemand(pd.DataFrame({ENERGY_FEATURE_NAME: [1, 2, 3]},
                                          index=pd.date_range('2023',periods=3,freq='D')))
    
    result_demand = composed_function(input_demand)
    
    expected_demand = MockTemporalHeatDemand(pd.DataFrame({ENERGY_FEATURE_NAME: [4, 6, 8]},
                                          index=pd.date_range('2023',periods=3,freq='D')))
    assert result_demand.data.equals(expected_demand.data)

def test_disaggregate_temporal_demand():
    # Test if disaggregate_temporal_demand applies functions correctly
    input_demand = MockTemporalHeatDemand(pd.DataFrame({ENERGY_FEATURE_NAME: [1, 2, 3]},
                                          index=pd.date_range('2023',periods=3,freq='D')))
    
    result_demand = disaggregate_temporal_demand(input_demand, [multiply_by_two_demand, add_one_demand])
    
    expected_demand = MockTemporalHeatDemand(pd.DataFrame({ENERGY_FEATURE_NAME: [4, 6, 8]},
                                          index=pd.date_range('2023',periods=3,freq='D')))
    
    assert result_demand.data.equals(expected_demand.data)

    # Test when no functions are provided
    result_demand_no_functions = disaggregate_temporal_demand(input_demand, [])
    
    assert result_demand_no_functions.data.equals(input_demand.data)
