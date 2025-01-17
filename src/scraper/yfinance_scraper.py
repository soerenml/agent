# Get the stock data
import yfinance as yf
import pandas as pd
from datetime import datetime

def calculate_rsi(df: pd.DataFrame, periods: int=14) -> pd.Series:
    """
    Calculate the Relative Strength Index (RSI) for a given DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the stock data.
    - periods (int): The number of periods to consider for calculating RSI. Default is 14.

    Returns:
    - rsi (pd.Series): The calculated RSI values.

    """
    # Calculate the price change (difference between each closing price)
    delta = df['Close'].diff()

    # Separate the gains and the losses
    gain = (delta.where(delta > 0, 0))
    loss = (-delta.where(delta < 0, 0))

    # Calculate the average gain and loss over the periods (usually 14 days)
    avg_gain = gain.rolling(window=periods, min_periods=1).mean()
    avg_loss = loss.rolling(window=periods, min_periods=1).mean()

    # Calculate the relative strength (RS)
    rs = avg_gain / avg_loss

    # Calculate the RSI using the formula
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_macd(df, short_period: int=5, long_period: int=35, signal_period: int=5):
    """
    Calculates the Moving Average Convergence Divergence (MACD) indicators for a given DataFrame.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing the stock data.
    - short_period (int): The number of periods for the short-term EMA. Default is 5.
    - long_period (int): The number of periods for the long-term EMA. Default is 35.
    - signal_period (int): The number of periods for the signal line EMA. Default is 5.

    Returns:
    - macd_line (pandas.Series): The MACD line.
    - signal_line (pandas.Series): The signal line.
    - macd_histogram (pandas.Series): The MACD histogram.
    """
    # Calculate the short-term (12-period) EMA
    short_ema = df['Close'].ewm(span=short_period, adjust=False).mean()

    # Calculate the long-term (26-period) EMA
    long_ema = df['Close'].ewm(span=long_period, adjust=False).mean()

    # Calculate the MACD line (difference between short and long EMA)
    macd_line = short_ema - long_ema

    # Calculate the Signal line (9-period EMA of the MACD line)
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()

    # Calculate the MACD histogram (difference between MACD line and Signal line)
    macd_histogram = macd_line - signal_line

    return macd_line, signal_line, macd_histogram


def download_yfinance_data(ticker_symbol: str,
                           start_date: datetime,
                           asset: str,
                           end_date: datetime) -> pd.DataFrame:
    """
    Downloads historical stock data for a given ticker symbol from Yahoo Finance and calculates technical indicators.

    Parameters:
    - ticker_symbol (str): The ticker symbol of the stock.
    - start_date (datetime): The start date of the data to download.
    - asset (str): The type of asset.
    - end_date (datetime): The end date of the data to download.
    - print_data (bool): Whether to print the downloaded data.

    Returns:
    - pd.DataFrame: A DataFrame containing the downloaded stock data with calculated technical indicators.
    """
    # Download the data
    yfinance_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval='1d')
    yfinance_data.columns = yfinance_data.columns.droplevel(1)  # Drops the second level ('BTC-USD')
    yfinance_data.reset_index(inplace=True) # Reset the index to have the 'Date' as a column

    # Modify the DataFrame to include the ticker symbol and asset type
    yfinance_data['ticker'] = ticker_symbol
    yfinance_data['asset'] = asset

    # Calculate the technical indicators
    yfinance_data['relative_strength_index'] = calculate_rsi(yfinance_data)
    yfinance_data['macd'], yfinance_data['signal_line'], yfinance_data['macd_histogram'] = calculate_macd(yfinance_data)

    yfinance_data = yfinance_data.rename(
        columns={'Price': 'price',
                 'Adj Close': 'adj_close',
                 'Close': 'close',
                 'High': 'high',
                 'Low': 'low',
                 'Open': 'open',
                 'Volume': 'volume',
                 'Date': 'date'})

    return yfinance_data