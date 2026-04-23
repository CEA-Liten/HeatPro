# tests/test_standard_profile.py
import pandas as pd
from heatpro.cold.standard_profile import (
    WeekProfile,
    WORKING_DAY_PROFILE,
    FULL_WEEK_PROFILE,
    StandardProfile,
)


def test_week_profile_description():
    # Test the description property of the WeekProfile class
    assert isinstance(WORKING_DAY_PROFILE.description, str)
    assert isinstance(FULL_WEEK_PROFILE.description, str)


def test_week_profile_function():
    # Test the function property of the WeekProfile class
    assert callable(WORKING_DAY_PROFILE.function)
    assert callable(FULL_WEEK_PROFILE.function)


def test_week_profile_week_series_example():
    # Test the week_series_example property of the WeekProfile class
    working_day_series = WORKING_DAY_PROFILE.week_series_example
    full_week_series = FULL_WEEK_PROFILE.week_series_example

    assert isinstance(working_day_series, pd.Series)
    assert isinstance(full_week_series, pd.Series)
    assert working_day_series.name == "week_profile_weigth"
    assert full_week_series.name == "week_profile_weigth"
    assert len(working_day_series) == 7 * 24
    assert len(full_week_series) == 7 * 24


def test_standard_profile_values():
    # Test the values of the StandardProfile enum
    assert StandardProfile.WORKING_DAY.value == WORKING_DAY_PROFILE
    assert StandardProfile.FULL_WEEK.value == FULL_WEEK_PROFILE


def test_standard_profile_iteration():
    # Test iteration over the StandardProfile enum
    for profile in StandardProfile:
        assert isinstance(profile, StandardProfile)
        assert isinstance(profile.value, WeekProfile)


def test_week_profile_function_output():
    # Test the output of the function property of the WeekProfile class
    working_day_function = WORKING_DAY_PROFILE.function
    full_week_function = FULL_WEEK_PROFILE.function

    # Test with different day of the week and hour
    test_cases = [
        (0, 0, 0.2),  # Monday, 00:00
        (0, 12, 1.0),  # Monday, 12:00
        (1, 0, 0.2),  # Tueasday, 00:00
        (1, 12, 1.0),  # Tueasday, 12:00
        (4, 0, 0.2),  # Friday, 00:00
        (4, 12, 1.0),  # Friday, 12:00
    ]

    for day_of_week, hour, expected in test_cases:
        assert working_day_function(day_of_week, hour) == expected
        assert full_week_function(day_of_week, hour) == expected

    assert working_day_function(5, 12) == 0.25
    assert full_week_function(5, 12) == 0.9
    assert working_day_function(6, 12) == 0.25
    assert full_week_function(6, 12) == 0.9
