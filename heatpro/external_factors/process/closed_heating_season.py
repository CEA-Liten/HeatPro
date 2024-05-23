import pandas as pd

from ..external_factors import ExternalFactors, HEATING_SEASON_NAME

CLOSED_HEATING_SEASON_NAME = f"closed_{HEATING_SEASON_NAME}"

def closed_heating_season(external_factor: ExternalFactors) -> pd.DataFrame:
    """Return a DataFrame with the same index than external_factor.data
    The DataFrame contains one column indicating True if the datatime is in a complete non-heating month.
    False otherwise.

    Args:
        external_factors (ExternalFactors): external factors class

    Returns:
        pd.DataFrame: DataFrame indicating the complete non-heating month
    """
    return pd.DataFrame(external_factor.data.groupby(external_factor.data.index.month)[HEATING_SEASON_NAME].transform('any'),
                      index=external_factor.data.index).rename({HEATING_SEASON_NAME:CLOSED_HEATING_SEASON_NAME},axis=1)