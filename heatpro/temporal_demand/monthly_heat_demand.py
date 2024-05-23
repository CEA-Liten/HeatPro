from matplotlib.axes import Axes
import pandas as pd

from . import TemporalHeatDemand
from ..check import find_duplicate_months

class MonthlyHeatDemand(TemporalHeatDemand):
    def __init__(self, name: str, data: pd.DataFrame) -> None:
        """
        Initialize an instance of MonthlyHeatDemand.

        Parameters:
            name (str): Name of the monthly heat demand.
            data (pd.DataFrame): DataFrame containing monthly heat demand data.

        Raises:
            ValueError: If the data index is not in datetime format.
            ValueError: If the required energy feature is not present in the data.
            ValueError: If there are duplicate months in the data index.
        """
        super().__init__(name, data)

        if not find_duplicate_months(data.index).empty:
            raise ValueError(f"Months {' ,'.join([f'{month.Month}-{month.Year}' for _, month in find_duplicate_months(data.index).iterrows()])} have multiple occurrences.")
