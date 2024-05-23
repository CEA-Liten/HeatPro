from matplotlib.axes import Axes
import pandas as pd

from . import TemporalHeatDemand
from ..check import find_duplicate_hours

class HourlyHeatDemand(TemporalHeatDemand):
    def __init__(self, name: str, data: pd.DataFrame) -> None:
        """
        Initialize an instance of HourlyHeatDemand.

        Parameters:
            name (str): Name of the hourly heat demand.
            data (pd.DataFrame): DataFrame containing hourly heat demand data.

        Raises:
            ValueError: If the data index is not in datetime format.
            ValueError: If the required energy feature is not present in the data.
            ValueError: If there are duplicate hours in the data index.
        """
        super().__init__(name, data)

        if not find_duplicate_hours(data.index).empty:
            raise ValueError(f"Hours {' ,'.join([f'{hour.Hour}:{hour.Day}-{hour.Month}-{hour.Year}' for _, hour in find_duplicate_hours(data.index).iterrows()])} have multiple occurrences.")