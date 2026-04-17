"""Module for managing profile for heat or cold demand."""

from typing import Callable

import pandas as pd


def step_night_reduction_week_profile(
    low: float, high_weekend: float, high_weekstart: float = 1.0
) -> Callable[[int, int], float]:
    """Creates a step function week profile for heat or cold demand.

    This function generates a week profile with different demand levels for weekdays and weekends.
    During weekdays (Monday to Friday), the demand is high from 8 AM to 6 PM, and low at other times.
    On weekends (Saturday and Sunday), the demand is high from 8 AM to 6 PM, but with a different
    high level than weekdays.

    Args:
        low: The low demand level (typically 0.0 for no demand).
        high_weekend: The high demand level for weekends.
        high_weekstart: The high demand level for weekdays (default is 1.0).

    Returns:
        A callable that takes day (0-6, where 0 is Monday) and hour (0-23) as input and returns
        the demand level for that time.
    """

    def week_profile(day: int, hour: int) -> float:
        if day in [5, 6]:  # On Weekend
            if 8 <= hour <= 18:
                return high_weekend
        if 8 <= hour <= 18:  # On Weekstart
            return high_weekstart
        return low

    return week_profile


def smooth_step_night_reduction_week_profile(
    low: float, high_weekend: float, high_weekstart: float = 1.0
) -> Callable[[int, int], float]:
    """Creates a smooth step function week profile for heat or cold demand.

    This function generates a week profile with different demand levels for weekdays and weekends,
    with smooth transitions between high and low demand periods. During weekdays (Monday to Friday),
    the demand is high from 10 AM to 5 PM, and low at other times. On weekends (Saturday and Sunday),
    the demand is high from 10 AM to 5 PM, but with a different high level than weekdays. The
    transition between high and low demand periods is smoothed over one hour.

    Args:
        low: The low demand level (typically 0.0 for no demand).
        high_weekend: The high demand level for weekends.
        high_weekstart: The high demand level for weekdays (default is 1.0).

    Returns:
        A callable that takes day (0-6, where 0 is Monday) and hour (0-23) as input and returns
        the demand level for that time.
    """

    def week_profile(day: int, hour: int) -> float:
        if day in [5, 6]:  # On Weekend
            if 10 <= hour <= 17:
                return high_weekend
            if hour == 9 or hour == 18:
                return 1 / 4 * low + 3 / 4 * high_weekend
            if hour == 8 or hour == 19:
                return 3 / 4 * low + 1 / 4 * high_weekend
        if 10 <= hour <= 17:  # On Weekstart
            return high_weekstart
        if hour == 9 or hour == 18:
            return 1 / 4 * low + 3 / 4 * high_weekstart
        if hour == 8 or hour == 19:
            return 3 / 4 * low + 1 / 4 * high_weekstart
        return low

    return week_profile


def apply_week_profile(
    datetime_index: pd.DatetimeIndex, week_profile: Callable[[int, int], float]
) -> pd.Series:
    """Applies a week profile to a datetime index.

    This function takes a datetime index and a week profile function, and returns a pandas Series
    with the demand levels for each datetime in the index. The week profile function is called
    with the day of the week (0-6, where 0 is Monday) and hour (0-23) for each datetime in the index.

    Args:
        datetime_index: A pandas DatetimeIndex representing the time period to apply the profile to.
        week_profile: A callable that takes day (0-6, where 0 is Monday) and hour (0-23) as input
            and returns the demand level for that time.

    Returns:
        A pandas Series with the demand levels for each datetime in the input index. The index of
        the Series is the same as the input datetime index, and the name of the Series is
        "week_profile_weigth".
    """
    return (
        pd.DataFrame(
            {"day": datetime_index.dayofweek, "hour": datetime_index.hour},
            index=datetime_index,
        )
        .apply(lambda row: week_profile(row.day, row.hour), axis=1)
        .rename("week_profile_weigth")
    )
