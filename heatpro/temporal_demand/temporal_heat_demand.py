from matplotlib.axes import Axes
import pandas as pd

from ..check import check_datetime_index, check_energy_feature, ENERGY_FEATURE_NAME

class TemporalHeatDemand:
    def __init__(self, name: str, data: pd.DataFrame) -> None:
        """
        Initialize an instance of TemporalHeatDemand.

        Parameters:
            name (str): Name of the heat demand.
            data (pd.DataFrame): DataFrame containing temporal heat demand data.

        Raises:
            ValueError: If the data index is not in datetime format.
            ValueError: If the required energy feature is not present in the data.
        """
        if not check_datetime_index(data):
            raise ValueError("data index should be in datetime format")
        if not check_energy_feature(data):
            raise ValueError(f"data has no {ENERGY_FEATURE_NAME} (required)")

        self.name = name
        self._data = data

    @property
    def data(self) -> pd.DataFrame:
        """
        Get the temporal heat demand data.

        Returns:
            pd.DataFrame: DataFrame containing temporal heat demand data.
        """
        return self._data

    def plot(self) -> Axes:
        """
        Plot the temporal heat demand data.

        Returns:
            Axes: The matplotlib Axes object for the plot.
        """
        return self._data.plot()
