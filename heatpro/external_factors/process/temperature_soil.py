import numpy as np
import pandas as pd

from .utils import get_coldest_dayofyear
from ..external_factors import ExternalFactors

SOIL_TEMPERATURE_NAME = 'soil_temperature'

def kasuda_soil_temperature(external_factor: ExternalFactors, d: float, alpha: float) -> pd.DataFrame:
    r"""
    Calculate Kasuda soil temperature based on external factors using (Kusada et al., 1965) approach.

    Parameters:
        external_factor (ExternalFactors): External factors data.
        d (float): Depth of pipes (meter).
        alpha (float): thermal diffusivity of the soil (meter²/day)

    Returns:
        pd.DataFrame: DataFrame containing the calculated Kasuda soil temperature.
        
    **Overview**
    
    
    .. math::
    
        T^{(\text{soil})}_t = \bar{T}^{(\text{External})} - \Delta_{month}T^{(\text{External})} \cdot \exp (-d\cdot \sqrt{\frac{\pi}{365 \cdot \alpha}}) \cdot \\ \cos(\frac{2\pi}{365}\cdot (t.day - t_{\text{coldest day of year}} - \frac{d}{2}\cdot \sqrt{\frac{\pi}{365 \cdot \alpha}}))
        
    where :math:`\Delta_{month}T^{(\text{External})}` is the average monthly amplitude over the years.
    """
    # Create an empty DataFrame with the same index as external_factor
    df = pd.DataFrame(index=external_factor.data.index, columns=[SOIL_TEMPERATURE_NAME])

    # Calculate average external temperature, average monthly amplitude, and coldest day of the year
    average_external_temperature = external_factor.data.external_temperature.mean()
    average_monthly_amplitude = 0.5 * external_factor.data.external_temperature.resample('MS').mean().resample('YS').apply(lambda x: x.max() - x.min()).mean()
    coldest_dayofyear = get_coldest_dayofyear(external_factor)

    # Calculate Kasuda soil temperature using the specified formula
    df[SOIL_TEMPERATURE_NAME] = average_external_temperature - average_monthly_amplitude * np.exp(-d*(np.pi/(365*alpha))**0.5) \
                            * np.cos(2*np.pi/365 *(df.index.dayofyear - coldest_dayofyear - d/2*(365/(np.pi*alpha))**0.5))

    return df

