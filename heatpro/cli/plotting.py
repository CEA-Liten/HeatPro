import pandas as pd
import plotly.graph_objects as go


def cold_results(weather: pd.Series, result: pd.DataFrame) -> go.Figure:
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
