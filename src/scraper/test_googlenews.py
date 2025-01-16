from scraper.googlenews import scrape
import unittest

class TestScrapeFunctionWithRealURL(unittest.TestCase):
    def test_scrape_real_url(self):
        # Use a real Google News URL
        url = "https://news.google.com/search?q=bitcoin&hl=en-US&gl=US&ceid=US%3Aen"

        # Call the scrape function
        headlines = scrape(url)

        # Check if the result is a non-empty list
        self.assertIsInstance(headlines, list, "Output should be a list")
        self.assertGreater(len(headlines), 0, "The list of headlines should not be empty")

        print(headlines[:10])

if __name__ == '__main__':
    unittest.main()