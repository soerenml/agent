import requests
from bs4 import BeautifulSoup

def scrape(url: str, printi: bool) -> list:
    """
    Scrape data from Google News
    """
    html_content = requests.get(url).content
    soup = BeautifulSoup(html_content, 'html.parser')
    headlines = soup.find_all('a', class_='JtKRv')
    all_headlines = [i.text for i in headlines]

    if printi:
        print(all_headlines)

    return all_headlines[:10]

scrape(
    url="https://news.google.com/search?for=shiba+inu+coin&hl=en-US&gl=US&ceid=US%3Aen",
    printi=True
)