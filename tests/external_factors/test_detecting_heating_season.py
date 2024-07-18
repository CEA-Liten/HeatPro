import pytest
import pandas as pd
import numpy as np
from heatpro.external_factors import non_heating_season_basic  # Replace 'your_module' with the actual module name where the function is defined

# Helper function to generate test data
def generate_test_data():
    date_range = pd.date_range(start='2023-01-01', end='2023-12-31 23:00:00', freq='h')
    np.random.seed(0)  # For reproducibility
    temperatures = np.sin(np.linspace(0, 10 * np.pi, len(date_range))) * 10 + 15 + np.random.normal(0, 5, len(date_range))
    external_temperature = pd.Series(temperatures, index=date_range)
    return external_temperature

# Test cases
test_cases = [
    {'temperature_threshold': 20, 'hot_day_min_share': 0.8, 'expected_start': '2023-03-21', 'expected_end': '2023-04-20'},
    {'temperature_threshold': 15, 'hot_day_min_share': 0.5, 'expected_start': '2023-01-01', 'expected_end': '2023-12-31'},
    {'temperature_threshold': 10, 'hot_day_min_share': 0.2, 'expected_start': '2023-01-01', 'expected_end': '2023-12-31'},
    {'temperature_threshold': 5, 'hot_day_min_share': 0.1, 'expected_start': '2023-01-01', 'expected_end': '2023-12-31'},
]

@pytest.mark.parametrize("case", test_cases)
def test_non_heating_season_basic(case):
    external_temperature = generate_test_data()
    start, end = non_heating_season_basic(
        external_temperature=external_temperature,
        temperature_threshold=case['temperature_threshold'],
        hot_day_min_share=case['hot_day_min_share']
    )
    
    assert start.strftime('%Y-%m-%d') == case['expected_start']
    assert end.strftime('%Y-%m-%d') == case['expected_end']
