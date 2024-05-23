import numpy as np
import pandas as pd

from ..check import WEIGHT_NAME_REQUIRED

from .building_heating_profile import *
from .hot_water_profile import *
from .loss_profile import *

def month_length_proportionnal_weight(dates: pd.DatetimeIndex) -> pd.DataFrame:
    """Create a Dataframe attributing a weight to each datetime of the index
    the weight depends only of month and year of the datetime.
    The weight attributed to each datetime equals month length over year length

    Args:
        dates (pd.DatetimeIndex): DatetimeIndex (a month can appear multiple times)

    Returns:
        pd.DataFrame: DataFrame with correct format to be used as weight
    """
    return pd.DataFrame(
                            dates.daysinmonth / (365 + dates.is_leap_year),
                            index = dates,
                            columns = [WEIGHT_NAME_REQUIRED]
                        )
    
def day_length_proportionnal_weight(dates: pd.DatetimeIndex) -> pd.DataFrame:
    """Create a Dataframe attributing a weight to each datetime of the index
    the weight depends only of date and month of the datetime.
    The weight attributed to each datetime equals day length over month length

    Args:
        dates (pd.DatetimeIndex): DatetimeIndex (a date can appear multiple times)

    Returns:
        pd.DataFrame: DataFrame with correct format to be used as weight
    """
    return pd.DataFrame(
                            1 / (dates.daysinmonth),
                            index = dates,
                            columns = [WEIGHT_NAME_REQUIRED]
                        )
    
def apply_hourly_pattern(hourly_index: pd.DatetimeIndex, hourly_mapping: dict[int,float]) -> pd.DataFrame:
    """Provide a DataFrame with correct weight format to disaggregate daily load into hourly load with a daily pattern.

    Args:
        hourly_index (pd.DatetimeIndex): Index
        hourly_mapping (dict[int,float]): assiossate to each hour (int between 1 and 24) a weight (sum should equals one)

    Returns:
        pd.DataFrame: DataFrame weight correct format
    """
    return pd.DataFrame(
                            hourly_index.hour.map(hourly_mapping),
                            index = hourly_index,
                            columns = [WEIGHT_NAME_REQUIRED],
                        )
    
def apply_weekly_hourly_pattern(hourly_index: pd.DatetimeIndex, hourly_mapping: dict[tuple[int,int],float]) -> pd.DataFrame:
    """Provide a DataFrame with correct weight format to disaggregate daily load into hourly load with a hourlt weekly pattern.
    It is better to have weight sum on 24 hours equals to 1 instead of weight sum equals to 1 over a week because week are note always complete in a month. This can lead to false disaggregation.

    Args:
        hourly_index (pd.DatetimeIndex): Index
        hourly_mapping (dict[tuple[int,int],float]): assiossate to each hour and each day of week (int between 1 and 7, int between 1 and 24) a weight (sum should equals one over each day)

    Returns:
        pd.DataFrame: DataFrame weight correct format
    """
    return pd.DataFrame(
                            pd.Series(hourly_index,index = hourly_index,).apply(lambda x: hourly_mapping.get((x.dayofweek, x.hour), 1)),
                            columns = [WEIGHT_NAME_REQUIRED],
                        )