import pandas as pd
from heatpro.external_factors import kasuda_soil_temperature, ExternalFactors, SOIL_TEMPERATURE_NAME

# Sample data for testing
sample_data = pd.DataFrame(
    {
        "external_temperature": [10.0, 15.0, 20.0, 25.0, 30.0],
        "heating_season": [True, True, True, False, False],
    },
    index=pd.date_range("2022-01-01", periods=5, freq="D"),
)


def test_kasuda_soil_temperature():
    external_factors = ExternalFactors(
        temperature=sample_data["external_temperature"],
        heating_season=sample_data["heating_season"],
    )
    d, alpha = 1.0, 0.5
    result = kasuda_soil_temperature(external_factors, d, alpha)

    assert isinstance(result, pd.Series)
    assert SOIL_TEMPERATURE_NAME == result.name
    assert result.index.equals(sample_data.index)
