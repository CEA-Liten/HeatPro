import pandas as pd

from . import check_datetime_index

WEIGHT_NAME_REQUIRED = "weight"

def check_weight_format(weights: pd.DataFrame) -> None:
    """Verify that DataFrame format is correct to be used as weight for potentially future disaggregation.

    Args:
        weights (pd.DataFrame): DataFrame having to role of containing weights

    Raises:
        ValueError: Should have DatetimeIndex
        ValueError: Should contain WEIGHT_NAME_REQUIRED column
    """
    if not check_datetime_index(weights):
        raise ValueError("data index should be in datetime format")
    
    if not WEIGHT_NAME_REQUIRED in weights.columns:
        raise ValueError(f"Months weights must be contained in a column named {WEIGHT_NAME_REQUIRED} of weights")
