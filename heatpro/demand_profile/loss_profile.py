import pandas as pd

from .building_heating_profile import WEIGHT_NAME_REQUIRED

from ..external_factors.induced_factors import InducedFactors

DELTA_TEMPERATURE_NAME = "delta_temperature"


def Y_to_H_thermal_loss_profile(temperatures: InducedFactors) -> pd.DataFrame:
    r"""Create an hourly heating building profile adjusted to districtit heating network temperatures and soil temperature. With sum over a year equals to 1.

    Args:
        temperatures (InducedFactors): hourly induced factors like supply/return temperature and soil temperature.

    Returns:
        pd.DataFrame: Dataframe correct weight format sum over a year equals to 1.

    **Overview**

    .. math::

        P^{(Loss)}_t = \frac{\frac{T^{(departure)}_t + T^{(return)}_t}{2} - T^{(soil)}_t}{\int_{t.year}\frac{T^{(departure)}_s + T^{(return)}_s}{2} - T^{(soil)}_s}

    where :

    :math:`T^{(soil)}_t` : Soil temperature

    :math:`T^{(departure)}_t` : District heating network departure temperature

    :math:`T^{(return)}_t` : District heating network return temperature

    """
    temperature_delta = (
        temperatures.supply_temperature + temperatures.return_temperature
    ) / 2 - temperatures.soil_temperature

    temperature_delta = temperature_delta.resample("h").sum()

    weights = pd.DataFrame(columns=[WEIGHT_NAME_REQUIRED])

    weights[WEIGHT_NAME_REQUIRED] = temperature_delta / temperature_delta.resample("YE").transform(
        "sum"
    )

    return weights
