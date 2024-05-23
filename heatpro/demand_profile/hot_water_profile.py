import numpy as np
import pandas as pd

from ..external_factors.process.temperature_cold_water import COLD_WATER_TEMPERATURE_NAME
from ..check import WEIGHT_NAME_REQUIRED, check_weight_format
from ..check import find_xor_months

def basic_hot_water_monthly_profile(cold_water_temperature: pd.DataFrame,T_prod: float,
                            monthly_HW_weight: pd.DataFrame) -> pd.DataFrame:
    r"""Create an monthly heating building profile adjusted to cold water temperature. With sum over a year equals to 1.

    Args:
        cold_water_temperature (pd.DataFrame): Cold water temperature. Can be hourly but not necessary
        T_prod (float): Hot water temperature
        monthly_HW_weight (pd.DataFrame): Initial month weight (often length proportionnal)

    Raises:
        ValueError: If some month are not present in both cold_water_temperature and monthly_HW_weight index

    Returns:
        pd.DataFrame: DataFrame monthly weighted correct format
        
    **Overview**
    
    .. math::
    
        P_{m}^{\text{(Hot water,adjusted)}} = \frac{(T^{(\text{prod})}-\frac{1}{\Delta_m}\int_m T^{(\text{Cold water})}_t)\cdot P_{m}^{(\text{(Hot water,raw))}}}{\int_{m.year}(T^{(\text{prod})}-\frac{1}{\Delta_m}\int_m T^{(\text{Cold water})}_t)\cdot P_{m}^{(\text{(Hot water,raw))}}}
    
    where:
    
    :math:`\frac{1}{\Delta_m}\int_m T^{(\text{Cold water})}_t` is average cold water (potable water arriving by pipepline) average temperature on month :math:`m`.
    
    :math:`T^{(\text{prod})}` is hot water setpoint temperature.
    
    :math:`P_{m}^{(\text{(Hot water,raw))}}` is heat consumption for hot water profile over the years (:math:`\int_{year}P_{m}^{(\text{(Hot water,raw))}})=1`)
    
    """
    monthly_cold_water = cold_water_temperature[[COLD_WATER_TEMPERATURE_NAME]].resample('MS').mean()
    
    if not find_xor_months(cold_water_temperature,monthly_HW_weight).empty:
        raise ValueError(f"cold_water_temperature and monthly_HW_weight index do not match \n not matching month: \n {find_xor_months(cold_water_temperature,monthly_HW_weight)}")
    
    monthly_cold_water.set_index(monthly_cold_water.index.to_period('M').start_time, inplace = True)
    monthly_HW_weight.set_index(monthly_HW_weight.index.to_period('M').start_time, inplace = True)
    
    monthly_hot_water_profil = monthly_HW_weight.copy()
    
    intermediary_name= 'weighted_delta_temperature'

    df = pd.DataFrame(monthly_HW_weight[WEIGHT_NAME_REQUIRED] * (T_prod - monthly_cold_water[COLD_WATER_TEMPERATURE_NAME]), columns=[intermediary_name], index=monthly_HW_weight.index)
    
    monthly_hot_water_profil[WEIGHT_NAME_REQUIRED] = df[intermediary_name] /\
                                                    df.groupby(df.index.year)[intermediary_name].transform('sum')
                                                    
    return monthly_hot_water_profil

def basic_hot_water_hourly_profile(raw_hourly_hotwater_profile: pd.DataFrame, simultaneity: float,
                                   sanitary_loop_coef: float) -> pd.DataFrame:
    r"""Create an hourly heating building profile adjusted to simultaneity and sanitary loop coef. With sum over a day equals to 1.
    
    Args:
        raw_hourly_hotwater_profile (pd.DataFrame): hourly profile sum of heating for hot water production
        simultaneity (float): coef between 0 and 1, 1 if consumption is simultaneous (leading to peak) and 0 if no simultaneity (leading to flat consumption)
        sanitary_loop_coef (float): share of heat used to keep sanitary loop hot.

    Returns:
        pd.DataFrame: DataFrame hourly weighted correct format
        
    **Overview**
    
    .. math::
    
        P_{t}^{(\text{Hot water,full adjusted})} = \frac{C^{(SL)}}{\Delta_{day}} + (1-C^{(SL)})\cdot (P_{t}^{(\text{Hot water,simultaneity adjusted})} +\\ 1 - \frac{1}{\Delta_{day}}) \int_{t.day} P_{s}^{(\text{Hot water,simultaneity adjusted})}
        
    where :
    
    .. math::
    
        P_{t}^{(\text{Hot water,simultaneity adjusted})} = \min(P_{t}^{\text{(Hot water,raw)}},S \cdot \underset{s\in t.day}{\max}P_{t}^{(\text{(Hot water,raw)})})
        
    :math:`S` : Coefficient between 0 and 1, 1 if consumption is simultaneous (leading to peak) and 0 if no simultaneity (leading to flat consumption)
    
    :math:`C^{(SL)}` : Share of heat used to keep sanitary loop hot.
    
    :math:`\frac{1}{\Delta_{day}} \int_{t.day} P_{s}^{(\text{Hot water,simultaneity adjusted})}` : Average over a day
    
    :math:`P_{t}^{\text{(Hot water,raw)}}` : Raw hourly profile heat consumption (:math:`\int_{day} P_{t}^{\text{(Hot water,raw)}} = 1`)
    
    """
    ajusted_hourly_hotwater_profile = pd.DataFrame(
                                                    np.minimum(
                                                        raw_hourly_hotwater_profile[WEIGHT_NAME_REQUIRED],
                                                        simultaneity * raw_hourly_hotwater_profile.groupby(raw_hourly_hotwater_profile.index.day)[WEIGHT_NAME_REQUIRED].transform('max')
                                                    ),
                                                    index = raw_hourly_hotwater_profile.index,
                                                    columns = [WEIGHT_NAME_REQUIRED],
                                                    )
    
    ajusted_hourly_hotwater_profile[WEIGHT_NAME_REQUIRED] = ajusted_hourly_hotwater_profile[WEIGHT_NAME_REQUIRED] + 1/24 - ajusted_hourly_hotwater_profile.groupby(ajusted_hourly_hotwater_profile.index.day)[WEIGHT_NAME_REQUIRED].transform('mean')
    
    ajusted_hourly_hotwater_profile[WEIGHT_NAME_REQUIRED] = sanitary_loop_coef/24 + (1-sanitary_loop_coef)*ajusted_hourly_hotwater_profile[WEIGHT_NAME_REQUIRED]
    
    return ajusted_hourly_hotwater_profile
    
                                                        
    
    