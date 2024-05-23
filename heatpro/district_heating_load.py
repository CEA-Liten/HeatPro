import warnings

import pandas as pd

from .check import ENERGY_FEATURE_NAME
from .temporal_demand import HourlyHeatDemand
from .external_factors import ExternalFactors, DEPARTURE_TEMPERATURE_NAME, RETURN_TEMPERATURE_NAME

class DistrictHeatingLoad:
    def __init__(self, demands: list[HourlyHeatDemand], external_factors: ExternalFactors,
                 district_network_temperature: pd.DataFrame, delta_temperature: float, cp: float) -> None:
        """
        Initialize an instance of DistrictHeatingLoad.

        Parameters:
            demands (list[HourlyHeatDemand]): List of HourlyHeatDemand instances representing individual demands.
            external_factors (ExternalFactors): External factors data.
            district_network_temperature (pd.DataFrame): DataFrame containing district network temperature data.
            delta_temperature (float): Temperature difference in the district heating network.
            cp (float): Specific heat capacity.

        Raises:
            ValueError: If required columns are missing in district_network_temperature.
            ValueError: If the indices between external_factors and district_network_temperature do not match.
            ValueError: If the indices between HourlyHeatDemand instances and district_network_temperature do not match.
        """
        self.demands = {demand.name: demand.data for demand in demands}
        self.external_factors = external_factors
        self.delta_temperature = delta_temperature
        self.cp = cp

        # Check required columns in district_network_temperature
        if not {DEPARTURE_TEMPERATURE_NAME, RETURN_TEMPERATURE_NAME}.issubset(set(district_network_temperature.columns)):
            raise ValueError(f"district_network_temperature should have columns : {' ,'.join({DEPARTURE_TEMPERATURE_NAME, RETURN_TEMPERATURE_NAME})}")
        self.district_network_temperature = district_network_temperature

        # Check matching indices between external_factors and district_network_temperature
        if not external_factors.data.index.equals(district_network_temperature.index):
            raise ValueError("Index between external_factors and district_network_temperature are not matching")

        # Check matching indices between HourlyHeatDemand instances and district_network_temperature
        if not all(demand.data.index.equals(district_network_temperature.index) for demand in demands):
            raise ValueError("Index between HourlyHeatDemand and district_network_factors are not matching")

    def fit(self):
        """
        Fit the DistrictHeatingLoad model.

        Calculates the corrected flow rate and updates the district_network_temperature accordingly.

        Returns:
            None
        """
        total_demand = pd.concat([demand[ENERGY_FEATURE_NAME] for demand in self.demands.values()], axis=1).sum(axis=1)
        flow_rate = total_demand / (self.cp * (self.district_network_temperature[DEPARTURE_TEMPERATURE_NAME] - self.district_network_temperature[RETURN_TEMPERATURE_NAME]))

        min_flow_rate = (total_demand / (self.cp * (self.district_network_temperature[DEPARTURE_TEMPERATURE_NAME] - (self.district_network_temperature[RETURN_TEMPERATURE_NAME] + self.delta_temperature)))).min()
        max_flow_rate = (total_demand / (self.cp * (self.district_network_temperature[DEPARTURE_TEMPERATURE_NAME] - (self.district_network_temperature[RETURN_TEMPERATURE_NAME] - self.delta_temperature)))).max()

        corrected_flow_rate = flow_rate.clip(min_flow_rate, max_flow_rate)

        self.district_network_temperature[RETURN_TEMPERATURE_NAME] = self.district_network_temperature[DEPARTURE_TEMPERATURE_NAME] - \
                                                                     total_demand / self.cp / corrected_flow_rate

        self.data = pd.concat(
            [self.external_factors.data, self.district_network_temperature] +
            [demand.rename(lambda x: f"{name}_{x}", axis=1) for name, demand in self.demands.items()],
            axis=1
        )
        
        
        
            