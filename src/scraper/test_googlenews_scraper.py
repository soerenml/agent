import pytest
from googlenews_scraper import scrape

def test_scrape_real_url():
    # Use a real Google News URL
    url = "https://news.google.com/search?q=bitcoin&hl=en-US&gl=US&ceid=US%3Aen"

    # Call the scrape function
    headlines = scrape(url)

    # Check if the result is a non-empty list
    assert isinstance(headlines, list), "Output should be a list"
    assert len(headlines) > 0, "The list of headlines should not be empty"

    print(f"\n Headlines extracted: \n\n\n {headlines[:10]}\n\n\n")
