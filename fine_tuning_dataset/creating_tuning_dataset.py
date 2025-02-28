import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf

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

    yfinance_data = yfinance_data.rename(
        columns={'Price': 'price',
                 'Adj Close': 'adj_close',
                 'Close': 'close',
                 'High': 'high',
                 'Low': 'low',
                 'Open': 'open',
                 'Volume': 'volume',
                 'Date': 'date'})

    yfinance_data['perc_change'] = yfinance_data['close'].pct_change() * 100

    return yfinance_data


df = download_yfinance_data(
    ticker_symbol="BTC-USD",
    start_date=datetime.today().date() - timedelta(days=60),
    asset="bitcoin",
    end_date=datetime.today().date()
    )

df = df[abs(df['perc_change']) > 2 ]

def trade_signal(value):
    if value < -2:
        return 'Sell'
    elif value > 2:
        return 'Buy'
    else:
        return 'Hold'  # If value is between -2 and 2

# Apply the function to the 'Value' column
df['signal'] = df['perc_change'].apply(trade_signal)
df = df[['date', 'signal', 'perc_change']]

for index, row in df.iterrows():
    new_date = (row['date'] - timedelta(days=1)).strftime('%Y-%m-%d')
    print(new_date, row['signal'], row['perc_change'])