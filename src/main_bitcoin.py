import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
import argparse

# Import Google news scraper module
from scraper.googlenews_scraper import scrape

# Import Yahoo finance scraper module
from scraper.yfinance_scraper import download_yfinance_data

# Import technical indicators module
from scraper.bitcoin_tech import get_data

# Import plot module for financial data
from helper.plotter import plot_technical_indicators

# Import finance_news_analyst agent module to analyze news
from agents import finance_news_analyst

# Import finance_data_analyst agent module to analyze financial data
from agents import finance_data_analyst

# Import technical_data_analyst agent module to analyze technical data
from agents import technical_data_analyst

# Import head_analyst agent module to analyse the results of the other agents
from agents import head_analyst


# Load the environment variables
load_dotenv()

parser = argparse.ArgumentParser(description="Bitcoin trader")

# By default the script always runs in production mode
parser.add_argument(
    "--test_run",
    "-n", type=str,
    default="False",
    help="Run in test or production mode"
)
args = parser.parse_args()


def run_main(args):
    TEST_RUN = args.test_run

    ASSET = "bitcoin"
    TICKER_SYMBOL = "BTC-USD"

    if TEST_RUN=="True":
        model = "gpt-3.5-turbo"
        print(f"\n\n\nTEST RUN! - {model}\n\n\n")
    else:
        model = "o1-preview"
        print(f"\n\n\nPRODUCTION RUN - {datetime.now():%Y-%m-%d} - {model}\n\n\n")

    # Initialize the language model
    llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model=model)

    # Scrape news headlines
    all_headlines = scrape(url="https://news.google.com/search?q=bitcoin&hl=en-US&gl=US&ceid=US%3Aen")

    # Scrape yfinance data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    data = download_yfinance_data(ticker_symbol=TICKER_SYMBOL,
                                  start_date=start_date,
                                  asset=ASSET,
                                  end_date=end_date)

    # Scrape technical data
    data_tech = get_data(print_data=True)

    # Plot financial data
    plot_technical_indicators(data=data, data_tech=data_tech)

    # Use financial news analyst agent to analyze news
    prompt = "src/prompts/news_analyst.md"
    output_news_analyst = finance_news_analyst(prompt, all_headlines, llm)
    print(f"\n\n\n\n ======= News analyst ======= \n\n{output_news_analyst}\n\n\n\n")

    # Use financial data analyst agent to analyze financial data
    prompt = "src/prompts/financial_analyst.md"
    output_finance_analyst = finance_data_analyst(prompt=prompt, data=data, asset=ASSET, llm=llm)
    print(f"\n\n\n\n ======= Financial analyst ======= \n\n{output_finance_analyst}\n\n\n\n")

    # Use technical data analyst agent to analyze technical data
    prompt = "src/prompts/technical_analyst.md"
    output_technical_analyst = technical_data_analyst(prompt=prompt, data=data_tech, asset=ASSET, llm=llm)
    print(f"\n\n\n\n ======= Technical analyst ======= \n\n{output_technical_analyst}\n\n\n\n")

    # Use head analyst agent to analyze the results of the other agents
    date_time = datetime.now().strftime('%Y-%m-%d %H')
    prompt = "src/prompts/head_analyst.md"

    # Load the previous reports
    with open('reports/merged_report.md', 'r', encoding='utf-8') as file:
        historical_data = file.read()

    output_head_analyst = head_analyst(prompt=prompt,
                                       result_1=output_news_analyst,
                                       result_2=output_finance_analyst,
                                       result_3=output_technical_analyst,
                                       llm=llm,
                                       date=date_time,
                                       historical_data=historical_data,
                                       print_option=False)
    print(f"\n\n\n\n ======= Head analyst ======= \n\n{output_head_analyst}\n\n\n\n")

    # Save the report of the head analyst
    if TEST_RUN=="True":
        pass
    else:
        report = f"report-{datetime.now():%Y-%m-%d}.md"
        save_path = os.path.join('reports', report)
        os.makedirs('reports', exist_ok=True)
        with open(save_path, "w") as file:
            file.write(output_head_analyst)

if __name__ == "__main__":
    run_main(args=args)