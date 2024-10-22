import os
from dotenv import load_dotenv
from datetime import datetime, timedelta


# Load the environment variables
load_dotenv()

# ----------------- PARAMETERS -----------------
ASSET = "bitcoin"
if ASSET == "bitcoin":
    TICKER_SYMBOL = "BTC-USD"

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o")

# ----------------- Scrape news headlines -----------------
from scraper.googlenews import scrape
all_headlines = scrape(url="https://news.google.com/search?q=bitcoin&hl=en-US&gl=US&ceid=US%3Aen")

# ----------------- Analyze content -----------------
from agents import finance_news_analyst
prompt = "src/prompts/news.md"
result_1 = finance_news_analyst(prompt, all_headlines, llm)
print(f"\n\n\n\n ======= News analyst ======= \n\n{result_1}\n\n\n\n")

# ----------------- Scrape financial data -----------------
from scraper.yfinance import download_yfinance_data
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
data = download_yfinance_data(ticker_symbol=TICKER_SYMBOL, start_date=start_date,
                              end_date=end_date, asset=ASSET)

# ----------------- Plot financial data -----------------
from helper.plotter import plot_technical_indicators
plot_technical_indicators(data=data)

# ----------------- Analyze financial data -----------------
from agents import finance_data_analyst
prompt = "src/prompts/financial_analyst.md"
result_2 = finance_data_analyst(prompt, data, ASSET, llm)
print(f"\n\n\n\n ======= Financial analyst ======= \n\n{result_2}\n\n\n\n")

# ----------------- Head analyst -----------------
from agents import head_analyst
prompt = "src/prompts/head_analyst.md"
result_3 = head_analyst(prompt, result_1, result_2, llm)
print(f"\n\n\n\n ======= Head analyst ======= \n\n{result_3}\n\n\n\n")

report = f"report-{datetime.now():%Y-%m-%d}.md"
save_path = os.path.join('reports', report)
os.makedirs('reports', exist_ok=True)
with open(save_path, "w") as file:
    file.write(result_3)

