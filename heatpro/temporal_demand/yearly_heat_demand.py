from matplotlib.axes import Axes
import pandas as pd

from . import TemporalHeatDemand
from ..check import find_duplicate_years

class YearlyHeatDemand(TemporalHeatDemand):
    def __init__(self, name: str, data: pd.DataFrame) -> None:
        """
        Initialize an instance of YearlyHeatDemand.

        Parameters:
            name (str): Name of the yearly heat demand.
            data (pd.DataFrame): DataFrame containing yearly heat demand data.

        Raises:
            ValueError: If the data index is not in datetime format.
            ValueError: If the required energy feature is not present in the data.
            ValueError: If there are duplicate years in the data index.
        """
        super().__init__(name, data)

        if find_duplicate_years(data.index):
            raise ValueError(f"Years {' ,'.join([str(year) for year in find_duplicate_years(data.index)])} have multiple occurrences.")
