import pandas as pd
from heatpro.week_profile import (
    step_night_reduction_week_profile,
    smooth_step_night_reduction_week_profile,
    apply_week_profile,
)


def test_step_night_reduction_week_profile():
    # Test case 1: Weekend day and hour within the high_weekend range
    week_profile = step_night_reduction_week_profile(low=0.5, high_weekend=1.5, high_weekstart=1.0)
    assert week_profile(5, 10) == 1.5

    # Test case 2: Weekend day and hour outside the high_weekend range
    assert week_profile(5, 20) == 0.5

    # Test case 3: Weekstart day and hour within the high_weekstart range
    assert week_profile(0, 10) == 1.0

    # Test case 4: Weekstart day and hour outside the high_weekstart range
    assert week_profile(0, 20) == 0.5


def test_smooth_step_night_reduction_week_profile():
    # Test case 1: Weekend day and hour within the high_weekend range
    week_profile = smooth_step_night_reduction_week_profile(
        low=0.5, high_weekend=1.5, high_weekstart=1.0
    )
    assert week_profile(5, 12) == 1.5

    # Test case 2: Weekend day and hour at the transition points
    assert week_profile(5, 9) == 1 / 4 * 0.5 + 3 / 4 * 1.5
    assert week_profile(5, 18) == 1 / 4 * 0.5 + 3 / 4 * 1.5
    assert week_profile(5, 8) == 3 / 4 * 0.5 + 1 / 4 * 1.5
    assert week_profile(5, 19) == 3 / 4 * 0.5 + 1 / 4 * 1.5

    # Test case 3: Weekend day and hour outside the high_weekend range
    assert week_profile(5, 20) == 0.5

    # Test case 4: Weekstart day and hour within the high_weekstart range
    assert week_profile(0, 12) == 1.0

    # Test case 5: Weekstart day and hour at the transition points
    assert week_profile(0, 9) == 1 / 4 * 0.5 + 3 / 4 * 1.0
    assert week_profile(0, 18) == 1 / 4 * 0.5 + 3 / 4 * 1.0
    assert week_profile(0, 8) == 3 / 4 * 0.5 + 1 / 4 * 1.0
    assert week_profile(0, 19) == 3 / 4 * 0.5 + 1 / 4 * 1.0

    # Test case 6: Weekstart day and hour outside the high_weekstart range
    assert week_profile(0, 20) == 0.5


def test_apply_week_profile():
    # Create a sample datetime index
    datetime_index = pd.date_range(start="2022-01-01", periods=6, freq="7h")

    # Test case 1: Apply step_night_reduction_week_profile
    week_profile = step_night_reduction_week_profile(low=0.5, high_weekend=1.5, high_weekstart=1.0)
    result = apply_week_profile(datetime_index, week_profile)
    assert isinstance(result, pd.Series)
    assert result.name == "week_profile_weigth"
    assert len(result) == 6
    assert result.equals(
        pd.Series([0.5, 0.5, 1.5, 0.5, 0.5, 1.5], index=datetime_index, name="week_profile_weigth")
    )

    # Test case 2: Apply smooth_step_night_reduction_week_profile
    week_profile = smooth_step_night_reduction_week_profile(
        low=0.5, high_weekend=1.5, high_weekstart=1.0
    )
    result = apply_week_profile(datetime_index, week_profile)
    assert isinstance(result, pd.Series)
    assert result.name == "week_profile_weigth"
    assert len(result) == 6
