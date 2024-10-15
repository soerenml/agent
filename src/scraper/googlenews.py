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
    # Fetch the HTML content of the page
    html_content = requests.get(url).content

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    headlines = soup.find_all('a', class_='JtKRv')

    # Print all the headlines
    all_headlines = []
    for i in headlines:
        all_headlines.append(i.text)

    return all_headlines
    # Optionally, extract URLs of the news articles
    #for headline in headlines:
    #    print(f"https://news.google.com{headline['href'][1:]}")