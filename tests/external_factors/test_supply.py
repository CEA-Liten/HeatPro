import pandas as pd
from heatpro.external_factors import (
    basic_temperature_supply,
    ExternalFactors,
    TemperatureThreshold,
    Threshold,
    SUPPLY_TEMPERATURE_NAME,
)

# Sample data for testing
sample_data = pd.DataFrame(
    {
        "external_temperature": [10.0, 15.0, 20.0, 25.0, 30.0],
        "heating_season": [0, 1, 1, 0, 0],
    },
    index=pd.date_range("2022-01-01", periods=5, freq="D"),
)


def test_basic_temperature_departure():
    external_factors = ExternalFactors(
        temperature=sample_data["external_temperature"],
        heating_season=sample_data["heating_season"],
    )
    temperature_threshold = TemperatureThreshold(Threshold(10, 30), Threshold(5, 20), 25, 15)
    result = basic_temperature_supply(external_factors, temperature_threshold)

    assert isinstance(result, pd.Series)
    assert SUPPLY_TEMPERATURE_NAME == result.name
    assert result.index.equals(sample_data.index)
