import importlib.metadata

__version__ = importlib.metadata.version("heatpro")

from .cold import COLD_OPERATING_MONTHS
from .check import ENERGY_FEATURE_NAME
from .demand_profile.building_heating_profile import BUILDING_FELT_TEMPERATURE_NAME
from .external_factors import (
    COLD_WATER_TEMPERATURE_NAME,
    SUPPLY_TEMPERATURE_NAME,
    RETURN_TEMPERATURE_NAME,
    SOIL_TEMPERATURE_NAME,
)

__all__ = [
    "COLD_OPERATING_MONTHS",
]

def help_with_feature_name():
    message = f"""
    Features names are set in package files.\n
    In order to propose a stable framework features names are required.\n
    Features names :\n
    {ENERGY_FEATURE_NAME = } , used for TemporalHeatDemand, import with from heatpro.check\n
    {BUILDING_FELT_TEMPERATURE_NAME = } , used to generate heating building profile, import with heatpro.demand_profile.building_heating_profile\n
    {COLD_WATER_TEMPERATURE_NAME = } , import with heatpro.external_factors \n
    {SUPPLY_TEMPERATURE_NAME = } , import with heatpro.external_factors \n
    {RETURN_TEMPERATURE_NAME = } , import with heatpro.external_factors \n
    {SOIL_TEMPERATURE_NAME = } , import with heatpro.external_factors \n
                """
    print(message)
