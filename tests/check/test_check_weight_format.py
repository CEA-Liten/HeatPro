import pandas as pd
import pytest
from heatpro.check import WEIGHT_NAME_REQUIRED, check_weight_format

# Fixture for a sample DataFrame with datetime index
@pytest.fixture
def sample_weights():
    return pd.DataFrame({WEIGHT_NAME_REQUIRED: [0.1, 0.2, 0.15, 0.25, 0.3]},
                        index=pd.date_range('2022-01-01', periods=5, freq='D'))

# Test check_weight_format
def test_check_weight_format(sample_weights):
    # Valid weights DataFrame
    check_weight_format(sample_weights)  # Should not raise any exception

    # Invalid weights DataFrame without datetime index
    invalid_weights_no_datetime = sample_weights.copy()
    invalid_weights_no_datetime.index = range(5)
    with pytest.raises(ValueError, match="data index should be in datetime format"):
        check_weight_format(invalid_weights_no_datetime)

    # Invalid weights DataFrame without the required column
    invalid_weights_no_column = sample_weights.drop(columns=[WEIGHT_NAME_REQUIRED])
    with pytest.raises(ValueError, match=f"Months weights must be contained in a column named {WEIGHT_NAME_REQUIRED} of weights"):
        check_weight_format(invalid_weights_no_column)
