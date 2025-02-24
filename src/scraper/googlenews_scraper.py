import requests
from bs4 import BeautifulSoup, SoupStrainer


def scrape(url: str) -> list:
    """
    Scrapes headlines from Google News page.

    Args:
        url (str): The URL of the Google News page.

    Returns:
        list: A list of headlines extracted from the page.
    """
    with requests.get(url) as response:
        html_content = response.content

    headlines = BeautifulSoup(
        html_content, 'html.parser',
        parse_only=SoupStrainer('a', class_='JtKRv')
    )
    return [headline.text for headline in headlines]
