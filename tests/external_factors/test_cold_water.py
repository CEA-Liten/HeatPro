import pandas as pd
import pytest
from heatpro.external_factors import burch_cold_water, ExternalFactors, COLD_WATER_TEMPERATURE_NAME

# Sample data for testing
sample_data = pd.DataFrame(
    {
        "external_temperature": [10.0, 15.0, 20.0, 25.0, 30.0],
        "heating_season": [
            True,
            True,
            True,
            False,
            False,
        ],
    },
    index=pd.date_range("2022-01-01", periods=5, freq="D"),
)


def test_burch_cold_water():
    external_factors = ExternalFactors(
        temperature=sample_data["external_temperature"],
        heating_season=sample_data["heating_season"],
    )
    result = burch_cold_water(external_factors)

    assert isinstance(result, pd.Series)
    assert COLD_WATER_TEMPERATURE_NAME == result.name
    assert result.index.equals(sample_data.index)


# Additional test for handling an empty DataFrame
def test_burch_cold_water_empty_dataframe():
    empty_data = pd.DataFrame(
        columns=["external_temperature", "heating_season"],
        index=pd.date_range("2022-01-01", periods=0, freq="D"),
    )
    external_factors = ExternalFactors(
        temperature=empty_data["external_temperature"],
        heating_season=empty_data["heating_season"],
    )
    with pytest.raises(ValueError, match="attempt to get argmin of an empty sequence"):
        burch_cold_water(external_factors)
