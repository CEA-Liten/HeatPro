from dataclasses import dataclass
from enum import Enum
from pathlib import Path
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


STEP_WORKING_DAY_PROFILE = WeekProfile(
    """Weekly consumption profile with consumption during working hours
only on working days.

    This profile is adapted for tertiary buildings without weekend activities
    such as schools, offices, and administrations.""",
    smooth_step_night_reduction_week_profile(0.2, 0.25, 1),
)

STEP_FULL_WEEK_PROFILE = WeekProfile(
    """Weekly consumption profile with step consumption during working hours
all week long.

    This profile is adapted for buildings in operation all week long
    such as EPHAD, hospitals, shops, and hotels.""",
    smooth_step_night_reduction_week_profile(0.2, 0.9, 1),
)

DATA_WORKING_DAY_PROFIL = pd.read_csv(
    Path(__file__).parent / "profile_working_day.csv", sep=";", index_col=[0, 1]
)

WORKING_DAY_PROFILE = WeekProfile(
    """Weekly consumption profile with consumption during working hours
only on working days.

    This profile is well adapted for tertiary buildings without weekend activities
    such as schools, offices, and administrations.
    Source: https://www.npro.energy/main/en/load-profiles/office""",
    lambda day, hour: DATA_WORKING_DAY_PROFIL.loc[(day, hour), "value"],
)

DATA_FULL_WEEK_PROFILE = pd.read_csv(
    Path(__file__).parent / "profile_full_week.csv", sep=";", index_col=[0, 1]
)

FULL_WEEK_PROFILE = WeekProfile(
    """Weekly consumption profile with consumption during working hours
all week long.

    This profile is well adapted for buildings in operation all week long
    such as EPHAD, hospitals, shops, and hotels.
    Source: https://www.npro.energy/main/en/load-profiles/shopping-center""",
    lambda day, hour: DATA_FULL_WEEK_PROFILE.loc[(day, hour), "value"],
)


class StandardProfile(Enum):
    """An enumeration of standard weekly consumption profiles.

    Attributes:
        STEP_WORKING_DAY (WeekProfile): Profile with step consumption only on working days.
        STEP_FULL_WEEK (WeekProfile): Profile with step consumption all week long.
    """

    STEP_WORKING_DAY = STEP_WORKING_DAY_PROFILE
    STEP_FULL_WEEK = STEP_FULL_WEEK_PROFILE
    WORKING_DAY = WORKING_DAY_PROFILE
    FULL_WEEK = FULL_WEEK_PROFILE


if __name__ == "__main__":
    print(DATA_WORKING_DAY_PROFIL)
