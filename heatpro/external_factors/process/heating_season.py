import pandas as pd

def non_heating_season_basic(external_temperature: pd.Series, temperature_threshold: float, hot_day_min_share: float) -> tuple[pd.Timestamp,pd.Timestamp]:
    r"""
    Determines the beginning and end dates of the non-heating season for a district heating network.

    The non-heating season is defined as the longest period during which the average hourly temperature remains above a certain threshold,
    with a minimum share of hot days (days with average temperature above the threshold) within that period.

    Args:
        external_temperature (pd.Series): A pandas Series containing the hourly average external temperature.
        temperature_threshold (float): The temperature threshold above which a day is considered a hot day.
        hot_day_min_share (float): The minimum share of hot days required for a period to be considered part of the non-heating season.

    Returns:
        tuple[pd.Timestamp,pd.Timestamp]: A tuple containing the beginning and end dates of the non-heating season as pandas Timestamps.
        
    **Overview**
    
    We define :
    
    .. bullet list:: 
    
    - :math:`(\bar{T}_{n})_{n\in\{1,\dots,365\}}` : the daily average outside temperature series (input is hourly time serie)
    - :math:`T_{threshold}` : the hot day temperature threshold, for :math:`n\in\{1,\dots,365\}` if :math:`\bar{T}_{n} > T_{threshold}` then day :math:`n` is a hot day, else it is a cold day
    - :math:`\sigma` : the minimal share of hot days the non-heating season must contain
    
    The function return :math:`n_{start},n_{end}\in\{1,\dots,365\}` defined as follow:
    
    .. math::

        n_{end} - n_{start}       
        
    subject to :
    
    .. math::

        n_{end} > n_{start}  
        
    .. math::

        \sum_{n\in\{n_{start},\dots,n_{end}\}} \mathbb{1}_{\bar{T}_{n}>T_{threshold}} \geq \sigma \cdot ( n_{end} - n_{start})
        
    :math:`n_{start},n_{end}` are found by testing all the combinations given that days :math:`n_{start} and  :math:`n_{end}` are hot days next to cold days.
    
    """
    # Resample the series to daily average temperatures
    daily_temps = external_temperature.resample('D').mean()
    
    # Identify days where the average temperature is above the threshold
    hot_days = (daily_temps > temperature_threshold).astype(int)
    
    # Initialize variables to keep track of the longest period of non-heating days
    max_length = 0
    best_start = None
    best_end = None
    
    # Iterate over the possible start days
    for start in range(len(hot_days)):
        if hot_days.iloc[start] == 1:
            # Count hot days and total days
            hot_day_count = 0
            total_days = 0
            
            for end in range(start, len(hot_days)):
                total_days += 1
                if hot_days.iloc[end] == 1:
                    hot_day_count += 1
                
                # Check if the current period meets the hot day share requirement
                if hot_day_count / total_days >= hot_day_min_share:
                    if total_days > max_length:
                        max_length = total_days
                        best_start = start
                        best_end = end
    
    if best_start is not None and best_end is not None:
        return daily_temps.index[best_start], daily_temps.index[best_end]
    else:
        return None, None