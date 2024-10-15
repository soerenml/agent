# Get the stock data
import yfinance as yf
import pandas as pd
from datetime import datetime

def download_yfinance_data(ticker_symbol: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:

    # Download the data
    bitcoin_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval='1d')
    print(pd.DataFrame(bitcoin_data).head())

    return bitcoin_data