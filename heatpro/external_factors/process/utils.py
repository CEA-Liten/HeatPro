import pandas as pd

from ..external_factors import ExternalFactors

def convert_serie_C_to_F(celsius_serie: pd.Series) -> pd.Series:
    """
    Convert a pandas Series from Celsius to Fahrenheit.

    Parameters:
        celsius_serie (pd.Series): Series containing temperatures in Celsius.

    Returns:
        pd.Series: Series with temperatures converted to Fahrenheit.
    """
    return celsius_serie * 9/5 + 32

def convert_serie_F_to_C(fahrenheit_serie: pd.Series) -> pd.Series:
    """
    Convert a pandas Series from Fahrenheit to Celsius.

    Parameters:
        fahrenheit_serie (pd.Series): Series containing temperatures in Fahrenheit.

    Returns:
        pd.Series: Series with temperatures converted to Celsius.
    """
    return (fahrenheit_serie - 32) * 5/9

def get_coldest_dayofyear(external_factors: ExternalFactors) -> int:
    """
    Get the day of the year with the coldest average daily temperature.

    Parameters:
        external_factors (ExternalFactors): External factors data containing daily temperatures.

    Returns:
        int: Day of the year with the coldest average daily temperature.
    """
    # Resample the external temperature to daily and calculate the mean
    df_average_daily_temperature = external_factors.data.external_temperature.resample('D').mean()
    
    # Find the day of the year with the minimum average daily temperature
    coldest_dayofyear = df_average_daily_temperature.idxmin().dayofyear

    return coldest_dayofyear