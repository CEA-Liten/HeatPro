import importlib.metadata

__version__ = importlib.metadata.version("heatpro")

from .check import ENERGY_FEATURE_NAME, WEIGHT_NAME_REQUIRED
from .demand_profile.building_heating_profile import BUILDING_FELT_TEMPERATURE_NAME
from .external_factors import (COLD_WATER_TEMPERATURE_NAME, 
                               DEPARTURE_TEMPERATURE_NAME,
                               RETURN_TEMPERATURE_NAME,
                               SOIL_TEMPERATURE_NAME,
                               EXTERNAL_TEMPERATURE_NAME,
                               HEATING_SEASON_NAME,
                               REQUIRED_FEATURES,
                               )

def help_with_feature_name():
    message = f"""
    Features names are set in package files.\n
    In order to propose a stable framework features names are required.\n
    Features names :\n
    {ENERGY_FEATURE_NAME = } , used for TemporalHeatDemand, import with from heatpro.check\n
    {WEIGHT_NAME_REQUIRED = } , used to have a common name for profile weights, import with from heatpro.check\n
    {REQUIRED_FEATURES = } , required features for ExternalFactorls, import with heatpro.external_factors \n
    {EXTERNAL_TEMPERATURE_NAME = } , import with heatpro.external_factors \n
    {HEATING_SEASON_NAME = } , import with heatpro.external_factors \n
    {BUILDING_FELT_TEMPERATURE_NAME = } , used to generate heating building profile, import with heatpro.demand_profile.building_heating_profile\n
    {COLD_WATER_TEMPERATURE_NAME = } , import with heatpro.external_factors \n
    {DEPARTURE_TEMPERATURE_NAME = } , import with heatpro.external_factors \n
    {RETURN_TEMPERATURE_NAME = } , import with heatpro.external_factors \n
    {SOIL_TEMPERATURE_NAME = } , import with heatpro.external_factors \n
                """
    print(message)