import os
from dotenv import load_dotenv
from datetime import datetime, timedelta


# Load the environment variables
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"),
                 model= "gpt-4")


# ----------------- Scrape news headlines -----------------
from scraper.googlenews import scrape

all_headlines = scrape(url="https://news.google.com/search?q=dell&hl=en-US&gl=US&ceid=US%3Aen")

# ----------------- Analyze content -----------------
from llm_analyzer.analyzer import llm_analyzer

prompt = "src/prompts/news.md"
result = llm_analyzer(prompt, all_headlines, llm)
print(result)

# ----------------- Scrape financial data -----------------
from scraper.yfinance import download_yfinance_data

end_date = datetime.now()
start_date = end_date - timedelta(days=365)
data = download_yfinance_data(ticker_symbol="DELL", start_date=start_date, end_date=end_date)

# ----------------- Plot financial data -----------------
from helper.plotter import plot_technical_indicators

plot_technical_indicators(data=data)