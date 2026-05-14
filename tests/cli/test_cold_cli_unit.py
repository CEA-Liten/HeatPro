import pytest
import pandas as pd


@pytest.mark.cli
def test_calculate_year_average_power():
    from heatpro.cli.cold import calculate_year_average_power

    # Create a sample weather data series
    dates = pd.date_range(start="2021-01-01", end="2024", freq="h", inclusive="left")
    weather_data = pd.Series(
        [21.0] * 365 * 24 + [24.0] * 365 * 24 + [27.0] * 365 * 24,  # Summer temperatures
        index=dates,
    )

    # Define the year energy reference and set temperature
    year_energy_reference = 1000.0
    set_temperature = 18.0

    # Calculate the year average power
    year_avg_power = calculate_year_average_power(
        weather_data, year_energy_reference, set_temperature
    )

    # Verify the output
    assert isinstance(year_avg_power, pd.Series)
    assert len(year_avg_power) == 3  # One value per year
    assert year_avg_power.index.year.unique().tolist() == [2021, 2022, 2023]
    assert year_avg_power.name == "year_average_power_kW"

    # Verify the values
    delta_ref = (21 - 18 + 24 - 18 + 27 - 18) / 3
    expected_values = [
        1000.0 * (21 - 18) / delta_ref,
        1000.0 * (24 - 18) / delta_ref,
        1000.0 * (27 - 18) / delta_ref,
    ]
    assert (year_avg_power * weather_data.resample("YS").count()).tolist() == pytest.approx(
        expected_values, rel=1e-3
    )
    assert (year_avg_power * weather_data.resample("YS").count()).mean() == pytest.approx(
        1000, rel=1e-3
    )
