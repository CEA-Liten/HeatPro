import pandas as pd

ENERGY_FEATURE_NAME = "thermal_energy_kWh"

def check_datetime_index(dataframe: pd.DataFrame) -> bool:
        """
        Check if the index of a DataFrame is in datetime format.

        Parameters:
            dataframe (pd.DataFrame): data
        Returns:
            True if the index is in datetime format, False otherwise.
        """
        return isinstance(dataframe.index, pd.DatetimeIndex)

def check_energy_feature(dataframe: pd.DataFrame) -> bool:
        """
        Check if the DataFrame contains a column with energy information.

        Args:
            dataframe (pd.DataFrame): data

        Returns:
            bool: True if column ENERGY_FEATURE_NAME is present, False otherwise
        """
        return ENERGY_FEATURE_NAME in dataframe.columns

def find_duplicate_years(datetime_index: pd.DatetimeIndex) -> list:
        return list(datetime_index.year.value_counts()[datetime_index.year.value_counts()>1].index)

def find_duplicate_months(datetime_index: pd.DatetimeIndex):
    """
    Find and return a DataFrame containing (year, month) tuples that appear more than once in the given DatetimeIndex.

    Parameters:
        datetime_index: pd.DatetimeIndex

    Returns:
        DataFrame with columns 'Year', 'Month' representing (year, month) tuples with multiple appearances.
    """
    # Create a DataFrame with Year and Month columns
    df = pd.DataFrame({'Year': datetime_index.year, 'Month': datetime_index.month})

    # Group by Year and Month, count occurrences, and filter duplicates
    duplicates_df = df[df.duplicated(subset=['Year', 'Month'], keep=False)].drop_duplicates(keep='first')

    return duplicates_df[['Year', 'Month']]

def find_duplicate_days(datetime_index: pd.DatetimeIndex):
    """
    Find and return a DataFrame containing (year, month, day) tuples that appear more than once in the given DatetimeIndex.

    Parameters:
        datetime_index: pd.DatetimeIndex

    Returns:
        DataFrame with columns 'Year', 'Month', 'Day' representing (year, month, day) tuples with multiple appearances.
    """
    # Create a DataFrame with Year and Month columns
    df = pd.DataFrame({'Year': datetime_index.year, 'Month': datetime_index.month, 'Day': datetime_index.day})

    # Group by Year and Month, count occurrences, and filter duplicates
    duplicates_df = df[df.duplicated(subset=['Year', 'Month', 'Day'], keep=False)].drop_duplicates(keep='first')

    return duplicates_df[['Year', 'Month', 'Day']]

def find_duplicate_hours(datetime_index: pd.DatetimeIndex):
    """
    Find and return a DataFrame containing (year, month, day, hour) tuples that appear more than once in the given DatetimeIndex.

    Parameters:
        datetime_index: pd.DatetimeIndex

    Returns:
        DataFrame with columns 'Year', 'Month', 'Day', 'Hour' representing (year, month, day, hour) tuples with multiple appearances.
    """
    # Create a DataFrame with Year and Month columns
    df = pd.DataFrame({'Year': datetime_index.year, 'Month': datetime_index.month, 'Day': datetime_index.day, 'Hour':datetime_index.hour})

    # Group by Year and Month, count occurrences, and filter duplicates
    duplicates_df = df[df.duplicated(subset=['Year', 'Month', 'Day', 'Hour'], keep=False)].drop_duplicates(keep='first')

    return duplicates_df[['Year', 'Month', 'Day', 'Hour']]

def find_xor_months(df_left: pd.DataFrame, df_right: pd.DataFrame) -> pd.DataFrame:
    """Find month that are not in both index

    Args:
        df_left (pd.DataFrame): left DataFrame
        df_right (pd.DataFrame): right DataFrame

    Returns:
        pd.DataFrame: Dataframe showing of month that are not in both index
    """
    df = pd.merge(
    pd.DataFrame({'Year':df_left.index.year,'Month':df_left.index.month}), 
    pd.DataFrame({'Year':df_right.index.year,'Month':df_right.index.month}), 
    on=['Year','Month'], 
    how='outer', 
    indicator=True)
    df.index = df.reset_index(drop=True).index
    return df[df['_merge']!='both']

def find_xor_dates(df_left: pd.DataFrame, df_right: pd.DataFrame) -> pd.DataFrame:
    """Find dates that are not in both index

    Args:
        df_left (pd.DataFrame): left DataFrame
        df_right (pd.DataFrame): right DataFrame

    Returns:
        pd.DataFrame: Dataframe showing of dates that are not in both index
    """
    df = pd.merge(
    pd.DataFrame({'Date':df_left.index.date}), 
    pd.DataFrame({'Date':df_right.index.date}), 
    on=['Date'], 
    how='outer', 
    indicator=True)
    df.index = df.reset_index(drop=True).index
    return df[df['_merge']!='both']

def find_xor_hour(df_left: pd.DataFrame, df_right: pd.DataFrame) -> pd.DataFrame:
    """Find hours that are not in both index

    Args:
        df_left (pd.DataFrame): left DataFrame
        df_right (pd.DataFrame): right DataFrame

    Returns:
        pd.DataFrame: Dataframe showing of hours that are not in both index
    """
    df = pd.merge(
    pd.DataFrame({'Date':df_left.index.date,'Hour':df_left.index.hour}), 
    pd.DataFrame({'Date':df_right.index.date,'Hour':df_right.index.hour}), 
    on=['Date'], 
    how='outer', 
    indicator=True)
    df.index = df.reset_index(drop=True).index
    return df[df['_merge']!='both']

