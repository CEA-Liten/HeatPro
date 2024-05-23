import pandas as pd
import numpy as np
import pytest
from heatpro.check import WEIGHT_NAME_REQUIRED

from heatpro.demand_profile import (month_length_proportionnal_weight,
                         day_length_proportionnal_weight, apply_hourly_pattern,
                         apply_weekly_hourly_pattern)

# Fixture for a sample DatetimeIndex
@pytest.fixture
def sample_datetime_index():
    return pd.date_range('2022-01-01', periods=24, freq='h')

# Test month_length_proportionnal_weight
def test_month_length_proportionnal_weight(sample_datetime_index):
    weights = month_length_proportionnal_weight(sample_datetime_index)
    assert WEIGHT_NAME_REQUIRED in weights.columns
    assert len(weights) == len(sample_datetime_index)

# Test day_length_proportionnal_weight
def test_day_length_proportionnal_weight(sample_datetime_index):
    weights = day_length_proportionnal_weight(sample_datetime_index)
    assert WEIGHT_NAME_REQUIRED in weights.columns
    assert len(weights) == len(sample_datetime_index)

# Test apply_hourly_pattern
def test_apply_hourly_pattern(sample_datetime_index):
    hourly_mapping = {0: 0.5, 6: 1.0, 12: 0.8, 18: 0.3}
    weights = apply_hourly_pattern(sample_datetime_index, hourly_mapping)
    assert WEIGHT_NAME_REQUIRED in weights.columns
    assert len(weights) == len(sample_datetime_index)

# Test apply_weekly_hourly_pattern
def test_apply_weekly_hourly_pattern(sample_datetime_index):
    weekly_hourly_mapping = {(0, 0): 0.2, (2, 12): 0.5, (5, 18): 0.8}
    weights = apply_weekly_hourly_pattern(sample_datetime_index, weekly_hourly_mapping)
    assert WEIGHT_NAME_REQUIRED in weights.columns
    assert len(weights) == len(sample_datetime_index)

# Additional tests can be added for edge cases or specific scenarios.
