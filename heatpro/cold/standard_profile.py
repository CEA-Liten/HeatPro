from dataclasses import dataclass
from enum import Enum
from typing import Callable

import pandas as pd

from ..week_profile import smooth_step_night_reduction_week_profile


@dataclass
class WeekProfile:
    """A class representing a weekly consumption profile.

    Attributes:
        description (str): A description of the profile.
        function (Callable[[int, int], float]): A function that calculates the profile value
            for a given day of the week and hour of the day.
    """

    description: str
    function: Callable[[int, int], float]

    @property
    def week_series_example(self) -> pd.Series:
        """Returns an example series of the weekly profile.

        This property generates a pandas Series representing the weekly profile
        for one week starting from Monday (2025-01-06).

        Returns:
            pd.Series: A series with datetime index and profile values.
        """
        return pd.Series(
            {
                date: self.function(date.day_of_week, date.hour)
                for date in pd.date_range("2025-01-06", freq="1h", periods=7 * 24)
            },
            name="week_profile_weigth",
        )


WORKING_DAY_PROFILE = WeekProfile(
    """Weekly consumption profile with consumption during working hours
only on working days.

    This profile is well adapted for tertiary buildings without weekend activities
    such as schools, offices, and administrations.""",
    smooth_step_night_reduction_week_profile(0.2, 0.25, 1),
)

FULL_WEEK_PROFILE = WeekProfile(
    """Weekly consumption profile with consumption during working hours
all week long.

    This profile is well adapted for buildings in operation all week long
    such as EPHAD, hospitals, shops, and hotels.""",
    smooth_step_night_reduction_week_profile(0.2, 0.9, 1),
)


class StandardProfile(Enum):
    """An enumeration of standard weekly consumption profiles.

    Attributes:
        WORKING_DAY (WeekProfile): Profile with consumption only on working days.
        FULL_WEEK (WeekProfile): Profile with consumption all week long.
    """

    WORKING_DAY = WORKING_DAY_PROFILE
    FULL_WEEK = FULL_WEEK_PROFILE
