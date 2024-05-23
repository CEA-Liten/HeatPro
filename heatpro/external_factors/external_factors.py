from matplotlib.axes import Axes
import pandas as pd

from ..check import check_datetime_index

EXTERNAL_TEMPERATURE_NAME = 'external_temperature'
HEATING_SEASON_NAME = 'heating_season'
REQUIRED_FEATURES = [
                        EXTERNAL_TEMPERATURE_NAME,
                        HEATING_SEASON_NAME,
                    ]

class ExternalFactors:
    def __init__(self, data_external_factors: pd.DataFrame) -> None:
        """Initialize an instance of ExternalFactors with external factors data.

        Parameters:
            data_external_factors (pd.DataFrame): External factors data.

        Raises:
            ValueError: If the required features are missing in the provided data.
            ValueError: If the data index is not in datetime format.
        """
        if not self.check_required_features(data_external_factors):
            raise ValueError(f"Missing required features, data_external_factors must contain columns: {', '.join(REQUIRED_FEATURES)}\n(to developer: required features set in REQUIRED_FEATURES)")

        if not check_datetime_index(data_external_factors):
            raise ValueError("data_external_factors index should be in datetime format")

        self._data = data_external_factors

    def check_required_features(self, dataframe: pd.DataFrame) -> bool:
        """Check if a DataFrame contains all the required features specified in REQUIRED_FEATURES.

        Parameters:
            dataframe (pd.DataFrame): External factors data.

        Returns:
            bool: True if all required features are present, False otherwise.
        """
        # Get the column names of the DataFrame
        dataframe_columns = dataframe.columns.tolist()

        # Check if all required features are present in the DataFrame
        return all(feature in dataframe_columns for feature in REQUIRED_FEATURES)

    @property
    def data(self) -> pd.DataFrame:
        """Get the external factors data.

        Returns:
            pd.DataFrame: External factors data.
        """
        return self._data

    def plot(self) -> Axes:
        """Plots the external factors profile data.

        Returns:
            Axes: The matplotlib Axes object for the plot.
        """
        return self._data.plot()
    
