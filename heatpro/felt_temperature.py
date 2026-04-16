import pandas as pd


def calculate_felt_temperature(outdoor_temperature: pd.Series) -> pd.Series:
    return outdoor_temperature.ewm(24).mean().rename("felt_temperature")
