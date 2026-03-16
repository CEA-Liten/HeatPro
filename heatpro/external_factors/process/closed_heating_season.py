import pandas as pd

from ..external_factors import ExternalFactors

CLOSED_HEATING_SEASON_NAME = "closed_heating_season"


def closed_heating_season(external_factor: ExternalFactors) -> pd.Series:
    """Return a Series with the same index than external_factor.data
    The Series contains one column indicating True if the datatime is in a complete non-heating month.
    False otherwise.

    Args:
        external_factors (ExternalFactors): external factors class

    Returns:
        pd.Series: Series indicating the complete non-heating month
    """
    return pd.Series(
        external_factor.heating_season.groupby(
            external_factor.heating_season.index.month
        ).transform("any"),
        index=external_factor.heating_season.index,
        name=CLOSED_HEATING_SEASON_NAME,
    )
