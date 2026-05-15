import pandas as pd
import plotly.graph_objects as go


def cold_results(weather: pd.Series, result: pd.DataFrame) -> go.Figure:
    """Create a Plotly figure showing cold consumption and outdoor temperature.

    This function generates an interactive Plotly figure that displays the total
    cold consumption and daily outdoor temperature over time. The figure uses two
    y-axes to show both metrics on the same plot.

    Args:
        weather (pd.Series): A pandas Series containing temperature data indexed by timestamp.
        result (pd.DataFrame): A pandas DataFrame containing cold consumption data with a
            'total_consumption_kW' column.

    Returns:
        go.Figure: A Plotly Figure object containing the visualization of cold consumption
            and outdoor temperature.
    """
    daily_temperature = weather.resample("d").mean()
    return go.Figure(
        [
            go.Scattergl(
                x=weather.index,
                y=result["total_consumption_kW"],
                name="Total cold consumption",
                yaxis="y1",
            ),
            go.Scattergl(
                x=daily_temperature.index,
                y=daily_temperature,
                name="Daily outdoor temperature",
                yaxis="y2",
                marker_color="#1f77b4",
                marker_opacity=0.5,
                line_dash="dash",
            ),
        ],
    ).update_layout(
        hovermode="x unified",
        yaxis=dict(
            title_text="Power (<b>kW</b>)",
        ),
        yaxis2=dict(
            title_text="Temperature (<b>°C</b>)",
            anchor="x",
            overlaying="y",
            side="right",
            range=[-5, 40],
        ),
    )
