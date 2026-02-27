import pandas as pd

from ..external_factors import ExternalFactors

CLOSED_HEATING_SEASON_NAME = "closed_heating_season"

def closed_heating_season(external_factor: ExternalFactors) -> pd.DataFrame:
    """Return a DataFrame with the same index than external_factor.data
    The DataFrame contains one column indicating True if the datatime is in a complete non-heating month.
    False otherwise.

    Args:
        external_factors (ExternalFactors): external factors class

    Returns:
        pd.DataFrame: DataFrame indicating the complete non-heating month
    """
    return pd.DataFrame(external_factor.heating_season.groupby(external_factor.heating_season.index.month).transform('any'),
                      index=external_factor.heating_season.index).rename({"heating_season":CLOSED_HEATING_SEASON_NAME},axis=1)