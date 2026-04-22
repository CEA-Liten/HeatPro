import pandas as pd


def calculate_felt_temperature(outdoor_temperature: pd.Series) -> pd.Series:
    """
    Calculate the felt temperature based on the outdoor temperature.

    The felt temperature is calculated using an exponential weighted moving average (EWMA)
    with a span of 24 hours. This method smooths the outdoor temperature data to provide
    a more representative felt temperature over time.

    Args:
        outdoor_temperature (pd.Series): A pandas Series containing the outdoor temperature
            values. The index should represent time, and the values should be in degrees Celsius.

    Returns:
        pd.Series: A pandas Series containing the calculated felt temperature values.
            The index will match the input series, and the values will be in degrees Celsius.
    """
    return outdoor_temperature.ewm(span=24).mean().rename("felt_temperature")
