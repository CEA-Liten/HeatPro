from typing import Callable

import pandas as pd


def step_night_reduction_week_profile(
    low: float, high_weekend: float, high_weekstart: float = 1.0
) -> Callable[[int, int], int]:
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
) -> Callable[[int, int], int]:
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
    datetime_index: pd.DatetimeIndex, week_profile: Callable[[int, int], int]
) -> pd.Series:
    return (
        pd.DataFrame(
            {"day": datetime_index.dayofweek, "hour": datetime_index.hour},
            index=datetime_index,
        )
        .apply(lambda row: week_profile(row.day, row.hour), axis=1)
        .rename("week_profile_weigth")
    )
