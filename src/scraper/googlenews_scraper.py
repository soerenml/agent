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

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    headlines = soup.find_all('a', class_='JtKRv')

    # Capture all headlines in a list
    all_headlines = [headline.text for headline in headlines]

    time.sleep(1)  # Small delay to be polite

    return all_headlines
    # Optionally, extract URLs of the news articles
    #for headline in headlines:
    #    print(f"https://news.google.com{headline['href'][1:]}")