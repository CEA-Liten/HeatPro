# tests/test_calculate_year_cold_needs.py
import json
from unittest.mock import patch, mock_open
import pytest
from heatpro.building_type import BuildingType
from heatpro.climatic_zone import ClimaticZone


mock_needs_data = {
    "data": {
        "zones_climatiques": {
            "H1a": {"Bureaux": 100, "EHPAD": 200},
            "H1b": {"Bureaux": 300, "EHPAD": 400},
        }
    }
}

# with patch("builtins.open", mock_open(read_data=json.dumps(mock_needs_data))):
# fait que toute ouverture de fichier par la fonction open ("builtins.open")
# va être emplacer ce qui sort de json.dumps(mock_needs_data)


def test_calculate_year_cold_needs():
    # Test with different building types and climatic zones
    test_cases = [
        (BuildingType("Bureaux"), ClimaticZone("H1a"), 10.0, 1000.0),
        (BuildingType("EHPAD"), ClimaticZone("H1a"), 10.0, 2000.0),
        (BuildingType("Bureaux"), ClimaticZone("H1b"), 10.0, 3000.0),
        (BuildingType("EHPAD"), ClimaticZone("H1b"), 10.0, 4000.0),
    ]

    with patch("builtins.open", mock_open(read_data=json.dumps(mock_needs_data))):
        from heatpro.cold.needs import calculate_year_cold_needs

        for building_type, climatic_zone, surface, expected in test_cases:
            result = calculate_year_cold_needs(building_type, climatic_zone, surface)
            assert result == expected, f"Failed for {building_type}, {climatic_zone}, {surface}"


def test_calculate_year_cold_needs_invalid_building_type():
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_needs_data))):
        from heatpro.cold.needs import calculate_year_cold_needs

        with pytest.raises(ValueError):
            calculate_year_cold_needs(BuildingType("invalid_type"), ClimaticZone("H1a"), 10.0)


def test_calculate_year_cold_needs_invalid_climatic_zone():
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_needs_data))):
        from heatpro.cold.needs import calculate_year_cold_needs

        with pytest.raises(ValueError):
            calculate_year_cold_needs(BuildingType("Bureaux"), ClimaticZone("invalid_zone"), 10.0)
