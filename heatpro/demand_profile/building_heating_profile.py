import pandas as pd

from ..check import WEIGHT_NAME_REQUIRED
from ..check import find_xor_hour

BUILDING_FELT_TEMPERATURE_NAME = 'felt_temperature'

def basic_building_heating_profile(felt_temperature: pd.DataFrame, non_heating_temperature: float,
                                   hourly_weight: pd.DataFrame) -> pd.DataFrame:
    r"""Create an hourly heating building consumption hourly profile adjusted to felt temperature. With sum over a month equals to 1.

    Args:
        felt_temperature (pd.DataFrame): Hourly felt temperature by building (to take into account inertia between outside cold and heating reactions)
        non_heating_temperature (float): Temperature above which felt_temperature does not activate heating
        hourly_weight (pd.DataFrame): Initial profile

    Raises:
        ValueError: felt_temperature and hourly_weight should have same index

    Returns:
        pd.DataFrame: DataFrame with correct weight format
        
    **Overview**

    .. math::
    
        P^{(\text{Heating building,adjusted})}_t = 
        \frac{\max(0,T^{(NH)}-T^{(\text{felt})}_t)\cdot P^{(\text{Heating building,raw})}_t}{\int_{t.month}\max(0,T^{(NH)}-T^{(\text{felt})}_t)\cdot P^{(\text{Heating building,raw})}_t}

    where:
    
    :math:`T^{(\text{felt})}_t` : Felt temperature by buildings different from external temperature because of inertia.
    
    :math:`T^{(NH)}` : Temperature above which :math:`T^{(\text{felt})}_t` emperature does not activate heating.

    :math:`P^{(\text{Heating building,raw})}_t` : Raw hourly profile (:math:`\int_{\text{day})}P^{(\text{Heating building,raw})}_t=1` but not mandatory because of normalisation)

    :math:`P^{(\text{Heating building,adjusted})}_t` : Adjusted hourly profile.
    
    :math:`t` is an instant (datetime) representing an hour, :math:`t.month` is month associated to instant :math:`t`
    
    """
    if not find_xor_hour(felt_temperature,hourly_weight).empty:
        raise ValueError(f"felt_temperature and hourly_weight hours are not match\n Difference (head(10)\n {find_xor_hour(felt_temperature,hourly_weight).head(10)}")
    
    felt_temperature.set_index(felt_temperature.index.to_period('h').start_time, inplace = True)
    hourly_weight.set_index(hourly_weight.index.to_period('h').start_time, inplace = True)
    
    hourly_heating_profile = hourly_weight.copy()
    
    _delta_felt_temperature_profile = (non_heating_temperature - felt_temperature[BUILDING_FELT_TEMPERATURE_NAME]).clip(0)
    
    hourly_heating_profile[WEIGHT_NAME_REQUIRED] = _delta_felt_temperature_profile *hourly_weight[WEIGHT_NAME_REQUIRED] /\
                                                (_delta_felt_temperature_profile * hourly_weight[WEIGHT_NAME_REQUIRED]).groupby([hourly_weight.index.year,hourly_weight.index.month]).transform('sum')
                                                
    hourly_heating_profile[WEIGHT_NAME_REQUIRED] = hourly_heating_profile[WEIGHT_NAME_REQUIRED].fillna(0)
                                                
    return hourly_heating_profile
