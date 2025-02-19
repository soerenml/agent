import pandas as pd
from yfinance_scraper import download_yfinance_data

def test_download_yfinance_data():
    ticker_symbol = "BTC-USD"
    start_date = "2021-01-01"
    end_date = "2021-12-31"
    asset = "bitcoin"

    # Call the scrape function
    data = download_yfinance_data(ticker_symbol, start_date, asset, end_date)

    # Check if the result is a non-empty DataFrame
    assert isinstance(data, pd.DataFrame), "Output should be a DataFrame"
    assert not data.empty, "The DataFrame should not be empty"

    print(f"{data.info()}\n{data.head()}")