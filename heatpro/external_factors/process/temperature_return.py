import pandas as pd

from ..external_factors import ExternalFactors

RETURN_TEMPERATURE_NAME = "return_temperature"


def basic_temperature_return(
    external_factor: ExternalFactors, T_HS: float, T_NHS: float
) -> pd.Series:
    r"""
    Calculate basic return temperature based on external factors.

    Parameters:
        external_factor (ExternalFactors): External factors data.
        T_HS (float): Return temperature during the heating season.
        T_NHS (float): Return temperature during the non-heating season.

    Returns:
        pd.Series: Series containing the calculated basic return temperature.

    **Overview**

    .. math::
        T^{(return)}_t = \mathbb{1}_{t \in HS}\cdot T^{(return)}_{HS} + \mathbb{1}_{t \in NHS}\cdot T^{(return)}_{NHS}

    """
    return (
        external_factor.heating_season * T_HS + (1 - external_factor.heating_season) * T_NHS
    ).rename(RETURN_TEMPERATURE_NAME)
