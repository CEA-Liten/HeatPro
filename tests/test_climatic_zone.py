from heatpro.climatic_zone import ClimaticZone


def test_climatic_zone_working():
    climatic_zone = ClimaticZone.H1C

    assert isinstance(climatic_zone, ClimaticZone)
