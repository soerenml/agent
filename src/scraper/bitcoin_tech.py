import pandas as pd
import requests
from functools import reduce

def fetch_data(url: str, value_column_name: str) -> pd.DataFrame:
    """
    Retrieves data from the given URL and returns it as a pandas DataFrame.

    Parameters:
    url (str): The URL of the API to retrieve the data from.
    value_column_name (str): The name of the value column in the resulting DataFrame.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the data with columns 'Timestamp' and the specified value column.

    Raises:
    requests.exceptions.RequestException: If the request fails.

    Example Usage:
    >>> url = "https://api.blockchain.info/charts/hash-rate?timespan=1year&format=json"
    >>> df = fetch_data(url, 'Hash Rate (TH/s)')
    >>> print(df)
           Timestamp  Hash Rate (TH/s)
    0     1609459200       135000000.0
    1     1609545600       140000000.0
    ...
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Failed to retrieve data: {e}")

    # Parse the JSON response
    data = response.json()['values']

    # Create a pandas DataFrame
    df = pd.DataFrame(data)

    # Convert the timestamp and rename the value column
    df['Timestamp'] = pd.to_datetime(df['x'], unit='s')
    df['Timestamp'] = df['Timestamp'].dt.date
    df.drop(columns=['x'], inplace=True)

    df['9-day'] = df['y'].rolling(window=9).mean()
    df['14-day'] = df['y'].rolling(window=14).mean()
    df['25-day'] = df['y'].rolling(window=25).mean()

    df.rename(columns={'9-day': f"{value_column_name}-9-day"}, inplace=True)
    df.rename(columns={'14-day': f"{value_column_name}-14-day"}, inplace=True)
    df.rename(columns={'25-day': f"{value_column_name}-25-day"}, inplace=True)
    df.rename(columns={'y': value_column_name}, inplace=True)


    return df

def get_data(print_data: bool = False) -> pd.DataFrame:
    # Fetch hash rate data
    hash_rate_df = fetch_data(
        url="https://api.blockchain.info/charts/hash-rate?timespan=1year&format=json",
        value_column_name='hash_rate'
    )

    # Fetch difficulty ribbon data
    difficulty_ribbon_df = fetch_data(
        url="https://api.blockchain.info/charts/difficulty?timespan=1year&format=json",
        value_column_name='difficulty_ribbon'
    )

    active_adresses_df = fetch_data(
        url = "https://api.blockchain.info/charts/n-unique-addresses?timespan=1year&format=json",
        value_column_name='active_addresses'
    )

    transaction_volume_df = fetch_data(
        url = "https://api.blockchain.info/charts/transactions-per-second?timespan=1year&format=json",
        value_column_name='transaction_volume'
    )

    dfs = [hash_rate_df, difficulty_ribbon_df, active_adresses_df, transaction_volume_df]
    merged_df = reduce(lambda left, right: pd.merge(left, right, on='Timestamp', how='outer'), dfs)

    if print_data:
        print(merged_df.head())
    else:
        pass

    return merged_df

