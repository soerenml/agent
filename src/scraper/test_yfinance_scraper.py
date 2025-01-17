from yfinance_scraper import calculate_rsi, calculate_macd, download_yfinance_data
import yfinance as yf
import unittest
import pandas as pd

class TestScrapeFunctionWithRealURL(unittest.TestCase):
    def test_download_yfinance_data(self):
        ticker_symbol = "BTC-USD"
        start_date = "2021-01-01"
        end_date = "2021-12-31"
        asset = "bitcoin"
        print_data = True

        # Call the scrape function
        data = download_yfinance_data(ticker_symbol,
                                      start_date,
                                      asset,
                                      end_date)

        # Check if the result is a non-empty list
        self.assertIsInstance(data, pd.DataFrame, "Output should be a DataFrame")
        self.assertGreater(len(data), 0, "The DataFrame should not be empty")

        print(f"{data.info()}\n{data.head()}")

if __name__ == '__main__':
    unittest.main()