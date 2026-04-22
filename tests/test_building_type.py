from heatpro.building_type import BuildingType


def test_building_type_working():
    building_type = BuildingType.RETAIL

    assert isinstance(building_type, BuildingType)
