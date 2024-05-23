import pandas as pd

from ..check import WEIGHT_NAME_REQUIRED

from ..external_factors.process.temperature_return import RETURN_TEMPERATURE_NAME
from ..external_factors.process.temperature_departure import DEPARTURE_TEMPERATURE_NAME
from ..external_factors.process.temperature_soil import SOIL_TEMPERATURE_NAME

DELTA_TEMPERATURE_NAME = 'delta_temperature'

def Y_to_H_thermal_loss_profile(temperatures: pd.DataFrame) -> pd.DataFrame:
    r"""Create an hourly heating building profile adjusted to districtit heating network temperatures and soil temperature. With sum over a year equals to 1.

    Args:
        temperatures (pd.DataFrame): hourly temperatures

    Returns:
        pd.DataFrame: Dataframe correct weight format sum over a year equals to 1.
        
    **Overview**
    
    .. math::
    
        P^{(Loss)}_t = \frac{\frac{T^{(departure)}_t + T^{(return)}_t}{2} - T^{(soil)}_t}{\int_{t.year}\frac{T^{(departure)}_s + T^{(return)}_s}{2} - T^{(soil)}_s}
    
    where :
    
    :math:`T^{(soil)}_t` : Soil temperature
    
    :math:`T^{(departure)}_t` : District heating network departure temperature
    
    :math:`T^{(return)}_t` : District heating network return temperature
    
    """
    temperature_delta = pd.DataFrame((temperatures[DEPARTURE_TEMPERATURE_NAME]+temperatures[RETURN_TEMPERATURE_NAME])/2 - temperatures[SOIL_TEMPERATURE_NAME],
                                     columns = [DELTA_TEMPERATURE_NAME])
    
    temperature_delta = temperature_delta.resample('h').sum()

    weights = pd.DataFrame(columns=[WEIGHT_NAME_REQUIRED])
    
    weights[WEIGHT_NAME_REQUIRED] = temperature_delta[DELTA_TEMPERATURE_NAME] /\
                                    temperature_delta[DELTA_TEMPERATURE_NAME].groupby(temperature_delta.index.year).transform('sum')
                                    
    return weights
    