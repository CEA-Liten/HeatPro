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
    return NEEDS["data"]["zones_climatiques"][climatic_zone.value][building_type.value] * surface
