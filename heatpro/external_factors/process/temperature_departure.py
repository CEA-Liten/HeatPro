import pandas as pd

from ..external_factors import ExternalFactors, EXTERNAL_TEMPERATURE_NAME, HEATING_SEASON_NAME

DEPARTURE_TEMPERATURE_NAME = 'departure_temperature'

def basic_temperature_departure(external_factor: ExternalFactors, T_max_HS: float,
                                T_max_NHS: float, T_min_HS: float,
                                T_min_NHS: float, T_ext_mid: float,
                                T_ext_min: float) -> pd.DataFrame:
    r"""
    Calculate basic temperature departure based on external factors.

    Parameters:
        external_factor (ExternalFactors): External factors data.
        T_max_HS (float): Maximum temperature during the heating season.
        T_max_NHS (float): Maximum temperature during the non-heating season.
        T_min_HS (float): Minimum temperature during the heating season.
        T_min_NHS (float): Minimum temperature during the non-heating season.
        T_ext_mid (float): Intermediate external temperature threshold.
        T_ext_min (float): Minimum external temperature threshold.

    Returns:
        pd.DataFrame: DataFrame containing the calculated basic temperature departure.
        
    **Overview**
    
    .. math::
        T^{(departure)}_t = \mathbb{1}_{T^{(ext)}_t<T^{(ext)}_{mid}} \frac{T^{(ext)}_t - T^{(ext)}_{mid}}{T^{(ext)}_{min} - T^{(ext)}_{mid}} \cdot (\mathbb{1}_{t \in HS}\cdot (T^{(departure)}_{HS,max} - T^{(departure)}_{HS,min}) + \\ \mathbb{1}_{t \in NHS}\cdot (T^{(departure)}_{NHS,max} - T^{(departure)}_{NHS,min})) + \mathbb{1}_{t \in HS}\cdot T^{(departure)}_{HS,min} + \mathbb{1}_{t \in NHS}\cdot T^{(departure)}_{NHS,min}
        
    """
    # Create an empty DataFrame with the same index as external_factor
    df = pd.DataFrame(index=external_factor.data.index, columns=[DEPARTURE_TEMPERATURE_NAME])

    # Calculate basic temperature departure using the specified formula
    df[DEPARTURE_TEMPERATURE_NAME] = (external_factor.data[EXTERNAL_TEMPERATURE_NAME] < T_ext_mid) *\
        (external_factor.data[EXTERNAL_TEMPERATURE_NAME] - T_ext_mid) /\
        (T_ext_min - T_ext_mid) *\
        (external_factor.data[HEATING_SEASON_NAME] * (T_max_HS - T_min_HS) +\
        (1 - external_factor.data[HEATING_SEASON_NAME]) * (T_max_NHS - T_min_NHS)) +\
        external_factor.data[HEATING_SEASON_NAME] * T_min_HS +\
        (1 - external_factor.data[HEATING_SEASON_NAME]) * T_min_NHS

    return df
                                