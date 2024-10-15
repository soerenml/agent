# Get the stock data
import yfinance as yf
import pandas as pd
from datetime import datetime

def download_yfinance_data(ticker_symbol: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:

    # Download the data
    yfinance_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval='1d')
    yfinance_data['Ticker'] = ticker_symbol
    print("\n\nyfinance data to be used\n\n")
    print(pd.DataFrame(yfinance_data).head())

    return yfinance_data