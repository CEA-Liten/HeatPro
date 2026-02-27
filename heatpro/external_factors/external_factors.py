from dataclasses import dataclass
import pandas as pd
import plotly.graph_objects as go

@dataclass
class ExternalFactors:
    temperature: pd.Series
    heating_season: pd.Series

    def __post_init__(self):
        if not isinstance(self.temperature.index, pd.DatetimeIndex):
            raise ValueError("temperature index must be a DatetimeIndex")

        if not isinstance(self.heating_season.index, pd.DatetimeIndex):
            raise ValueError("heating_season index must be a DatetimeIndex")

        if not self.temperature.index.equals(self.heating_season.index):
            raise ValueError("temperature and heating_season must have same index")

    def plot(self) -> go.Figure:
        """Plots the external factors profile data using Plotly.

        Returns:
            go.Figure: The Plotly Figure object for the plot.
        """
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.temperature.index,
            y=self.temperature,
            mode='lines',
            name='Outside Temperature',
        ))

        fig.add_trace(go.Scatter(
            x=self.heating_season.index,
            y=self.heating_season.astype(int),
            mode='lines',
            name='Heating Season',
        ))

        fig.update_layout(
            title='External Factors Profile',
            xaxis_title='Time',
            yaxis_title='Value',
            showlegend=True
        )

        return fig