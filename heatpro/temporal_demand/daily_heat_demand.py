from matplotlib.axes import Axes
import pandas as pd

from . import TemporalHeatDemand
from ..check import find_duplicate_days

class DailyHeatDemand(TemporalHeatDemand):
    def __init__(self, name: str, data: pd.DataFrame) -> None:
        """
        Initialize an instance of DailyHeatDemand.

        Parameters:
            name (str): Name of the daily heat demand.
            data (pd.DataFrame): DataFrame containing daily heat demand data.

        Raises:
            ValueError: If the data index is not in datetime format.
            ValueError: If the required energy feature is not present in the data.
            ValueError: If there are duplicate days in the data index.
        """
        super().__init__(name, data)

        if not find_duplicate_days(data.index).empty:
            raise ValueError(f"Days {' ,'.join([f'{day.Day}-{day.Month}-{day.Year}' for _, day in find_duplicate_days(data.index).iterrows()])} have multiple occurrences.")