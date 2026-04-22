import pandas as pd
import pytest

from heatpro.felt_temperature import calculate_felt_temperature


def test_calculate_felt_temperature():
    outdoor_temperature = pd.Series(
        [0] * 24 + [100] + [0] * 23,
        index=pd.date_range("2025-01-01", freq="1h", periods=48),
        name="outdoor_temperature",
    )
    felt_temperature = calculate_felt_temperature(outdoor_temperature)
    alpha = 2 / (1 + 24)
    hour_0 = felt_temperature.iloc[0]
    first_non_nul_hour = felt_temperature.iloc[24]
    last_hour = felt_temperature.iloc[-1]
    assert hour_0 == pytest.approx(0.0, abs=1e-9)
    assert first_non_nul_hour == pytest.approx(
        100 / sum((1 - alpha) ** k for k in range(25)), abs=1e-9
    )
    assert last_hour == pytest.approx(
        100 * (1 - alpha) ** 23 / sum((1 - alpha) ** k for k in range(48)), abs=1e-9
    )
