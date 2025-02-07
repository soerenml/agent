import time
import requests
from bs4 import BeautifulSoup


def scrape(url: str) -> list:
    """
    Scrapes headlines from Google News page.

    Args:
        url (str): The URL of the Google News page.

    Returns:
        list: A list of headlines extracted from the page.
    """

    html_content = requests.get(url).content
    soup = BeautifulSoup(html_content, 'html.parser')
    headlines = soup.find_all('a', class_='JtKRv')
    all_headlines = [headline.text for headline in headlines]
    time.sleep(1)  # Small delay to be polite

    return all_headlines