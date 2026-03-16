import pandas as pd

from ..check import ENERGY_FEATURE_NAME

pd.options.plotting.backend = 'plotly'

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
        if not isinstance(data.index,pd.DatetimeIndex):
            raise ValueError("data index should be in datetime format")
        if ENERGY_FEATURE_NAME not in data.columns:
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

    def plot(self):
        """
        Plot the temporal heat demand data.

        Returns:
            Axes: The matplotlib Axes object for the plot.
        """
        return self._data.plot()
