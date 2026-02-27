import pandas as pd
from heatpro.external_factors import (
    basic_temperature_return,
    ExternalFactors,
    RETURN_TEMPERATURE_NAME,
)

# Sample data for testing
sample_data = pd.DataFrame(
    {
        "external_temperature": [10.0, 15.0, 20.0, 25.0, 30.0],
        "heating_season": [0, 1, 1, 0, 0],
    },
    index=pd.date_range("2022-01-01", periods=5, freq="D"),
)


def test_basic_temperature_return():
    external_factors = ExternalFactors(
        temperature=sample_data["external_temperature"],
        heating_season=sample_data["heating_season"],
    )
    T_HS, T_NHS = 30, 20
    result = basic_temperature_return(external_factors, T_HS, T_NHS)

    assert isinstance(result, pd.Series)
    assert RETURN_TEMPERATURE_NAME == result.name
    assert result.index.equals(sample_data.index)
