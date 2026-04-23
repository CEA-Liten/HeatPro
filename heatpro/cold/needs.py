import json
from pathlib import Path

from ..building_type import BuildingType
from ..climatic_zone import ClimaticZone

with open(
    Path(__file__).parent / "needs_by_building_type_and_climatic_zone.json", "r", encoding="utf-8"
) as file:
    NEEDS = json.load(file)


def calculate_year_cold_needs(
    building_type: BuildingType, climatic_zone: ClimaticZone, surface: float
) -> float:
    """Calculate the annual cold needs for a building based on its type, climatic zone, and surface area.

    This function calculates the annual cold needs by multiplying the specific cold needs
    for the given building type and climatic zone by the building's surface area.

    Args:
        building_type (BuildingType): The type of building (e.g., residential, commercial).
        climatic_zone (ClimaticZone): The climatic zone where the building is located.
        surface (float): The surface area of the building in square meters.

    Returns:
        float: The annual cold needs in kilowatt-hours (kWh) for the building.
    """
    return NEEDS["data"]["zones_climatiques"][climatic_zone.value][building_type.value] * surface
