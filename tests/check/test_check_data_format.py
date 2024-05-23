import pandas as pd
import numpy as np
import pytest
from heatpro.check import (ENERGY_FEATURE_NAME, check_datetime_index, check_energy_feature,
                         find_duplicate_years, find_duplicate_months, find_duplicate_days,
                         find_duplicate_hours, find_xor_months, find_xor_dates, find_xor_hour)

# Fixture for a sample DataFrame with datetime index and energy feature
@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({ENERGY_FEATURE_NAME: [10, 20, 15, 25, 30]},
                        index=pd.date_range('2022-01-01', periods=5, freq='D'))
# Test check_datetime_index
def test_check_datetime_index(sample_dataframe):
    assert check_datetime_index(sample_dataframe)

# Test check_energy_feature
def test_check_energy_feature(sample_dataframe):
    assert check_energy_feature(sample_dataframe)

# Test find_duplicate_years
def test_find_duplicate_years():
    dates = pd.date_range('2022-01-01', periods=10, freq='D')
    datetime_index = pd.DatetimeIndex(dates)
    duplicate_years = find_duplicate_years(datetime_index)
    assert duplicate_years == [2022]

# Test find_duplicate_months
def test_find_duplicate_months():
    dates = pd.date_range('2022-01-01', periods=10, freq='D')
    datetime_index = pd.DatetimeIndex(dates)
    duplicate_months = find_duplicate_months(datetime_index)
    assert not duplicate_months.empty

# Test find_duplicate_days
def test_find_duplicate_days():
    dates = pd.date_range('2022-01-01', periods=10, freq='D')
    datetime_index = pd.DatetimeIndex(dates)
    duplicate_days = find_duplicate_days(datetime_index)
    assert duplicate_days.empty

# Test find_duplicate_hours
def test_find_duplicate_hours():
    dates = pd.date_range('2022-01-01', periods=10, freq='h')
    datetime_index = pd.DatetimeIndex(dates)
    duplicate_hours = find_duplicate_hours(datetime_index)
    assert duplicate_hours.empty

# Test find_xor_months
def test_find_xor_months(sample_dataframe):
    df_left = sample_dataframe.iloc[:3]
    df_right = sample_dataframe.iloc[2:]
    xor_months = find_xor_months(df_left, df_right)
    assert xor_months.empty

# Test find_xor_dates
def test_find_xor_dates(sample_dataframe):
    df_left = sample_dataframe.iloc[:3]
    df_right = sample_dataframe.iloc[2:]
    xor_dates = find_xor_dates(df_left, df_right)
    assert not xor_dates.empty

# Test find_xor_hour
def test_find_xor_hour(sample_dataframe):
    df_left = sample_dataframe.iloc[:3]
    df_right = sample_dataframe.iloc[2:]
    xor_hour = find_xor_hour(df_left, df_right)
    assert not xor_hour.empty
