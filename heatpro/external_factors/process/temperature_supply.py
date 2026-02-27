import pandas as pd

from ..external_factors import ExternalFactors
from ..temperature_threshold import TemperatureThreshold

SUPPLY_TEMPERATURE_NAME = "supply_temperature"


def basic_temperature_supply(
    external_factor: ExternalFactors, temperature_threshold: TemperatureThreshold
) -> pd.Series:
    r"""
    Calculate basic temperature supply based on external factors.

    Parameters:
        external_factor (ExternalFactors): External factors data.
        temperature_threshold (TemperatureThreshold): Temperatures threshold used to calculate supply temperature containing:

            - :math:`T^{(departure)}_{HS,max}` : Maximum temperature during the heating season.
            - :math:`T^{(departure)}_{NHS,max}` : Maximum temperature during the non-heating season.
            - :math:`T^{(departure)}_{HS,min}` : Minimum temperature during the heating season.
            - :math:`T^{(departure)}_{NHS,min}` : Minimum temperature during the non-heating season.
            - :math:`T^{(ext)}_{mid}` : Intermediate external temperature threshold.
            - :math:`T^{(ext)}_{min}` : Minimum external temperature threshold.

    Returns:
        pd.Series: Series containing the calculated basic temperature supply.

    **Overview**

    .. math::
        T^{(supply)}_t = \mathbb{1}_{T^{(ext)}_t<T^{(ext)}_{mid}} \frac{T^{(ext)}_t - T^{(ext)}_{mid}}{T^{(ext)}_{min} - T^{(ext)}_{mid}} \cdot (\mathbb{1}_{t \in HS}\cdot (T^{(departure)}_{HS,max} - T^{(departure)}_{HS,min}) + \\ \mathbb{1}_{t \in NHS}\cdot (T^{(departure)}_{NHS,max} - T^{(departure)}_{NHS,min})) + \mathbb{1}_{t \in HS}\cdot T^{(departure)}_{HS,min} + \mathbb{1}_{t \in NHS}\cdot T^{(departure)}_{NHS,min}

    """
    # Create an empty DataFrame with the same index as external_factor
    temperature_supply = (
        (external_factor.temperature < temperature_threshold.outside_mid)
        * (external_factor.temperature - temperature_threshold.outside_mid)
        / (temperature_threshold.outside_min - temperature_threshold.outside_mid)
        * (
            external_factor.heating_season
            * (temperature_threshold.heating_season.max - temperature_threshold.heating_season.min)
            + (1 - external_factor.heating_season)
            * (
                temperature_threshold.non_heating_season.max
                - temperature_threshold.non_heating_season.min
            )
        )
        + external_factor.heating_season * temperature_threshold.heating_season.min
        + (1 - external_factor.heating_season) * temperature_threshold.non_heating_season.min
    )

    return temperature_supply.rename(SUPPLY_TEMPERATURE_NAME)
