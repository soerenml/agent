from  ..scraper.yfinance_scraper import download_yfinance_data
from datetime import datetime, timedelta


df = download_yfinance_data(
    ticker_symbol="BTC-USD",
    start_date=datetime.today().date() - timedelta(days=60),
    asset="bitcoin",
    end_date=datetime.today().date()
    )

print(df.info)