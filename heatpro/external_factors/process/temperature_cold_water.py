import numpy as np
import pandas as pd

from .utils import convert_serie_C_to_F, convert_serie_F_to_C, get_coldest_dayofyear
from ..external_factors import ExternalFactors, EXTERNAL_TEMPERATURE_NAME

COLD_WATER_TEMPERATURE_NAME = 'cold_water_temperature'

def burch_cold_water(external_factors: ExternalFactors) -> pd.DataFrame:
    r"""
    Calculate the cold water temperature based on external factors using (Burch et al., 2007) approach.

    Parameters:
        external_factors (ExternalFactors): External factors data containing temperatures.

    Returns:
        pd.DataFrame: DataFrame containing the calculated cold water temperatures.
        
    **Overview**
    
    .. math::
    
        T^{(\text{Cold water})}_t = (\bar{T}^{(\text{External})} + 3) + ( 0.4 + 0.01 \cdot (0.01 \cdot(\bar{T}^{(\text{External})}-44)))\cdot\\ \frac{\Delta_{day}T^{(\text{External})}}{2} \cdot \sin(0.01745 \cdot (0.986(t.day - t_{\text{coldest day of year}} + 79 - \bar{T}^{(\text{External})})))
        
    where :
    
    :math:`\underset{day}{\max} (\underset{t \in day}{\max}T^{(\text{External})} - \underset{t \in day}{\min}T^{(\text{External})})` : Maximal amplitude in a day of the dataset.
    
    :math:`\bar{T}^{(\text{External})}` : Average external temperature over the dataset.
    
    """
    # Convert external temperature to Fahrenheit
    external_temperature_F = convert_serie_C_to_F(external_factors.data[EXTERNAL_TEMPERATURE_NAME])

    # Get the day of the year with the coldest average daily temperature
    coldest_dayofyear = get_coldest_dayofyear(external_factors)

    # Calculate the cold water temperature in Fahrenheit
    cold_water_temperature_F = external_temperature_F.mean() + 3 +\
        (0.4 + 0.01 * (external_temperature_F.mean() - 44)) / 2 *\
        external_temperature_F.resample('D').apply(lambda x: x.max() - x.min()).max() *\
        np.sin(0.01745 * (0.986 * (external_temperature_F.index.dayofyear - coldest_dayofyear - (35 - (external_temperature_F.mean() - 44))) - 90))

    # Convert cold water temperature back to Celsius and create DataFrame
    cold_water_temperature = pd.DataFrame(
        convert_serie_F_to_C(cold_water_temperature_F),
        columns=[COLD_WATER_TEMPERATURE_NAME],
        index=external_temperature_F.index
    )

    return cold_water_temperature