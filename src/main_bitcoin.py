import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
import subprocess
import sys

# Import Google news scraper module
from scraper.googlenews_scraper import scrape

# Import Yahoo finance scraper module
from scraper.yfinance_scraper import download_yfinance_data

# Import technical indicators module
from scraper.bitcoin_tech import get_data

# Import plot module for financial data
from helper.plotter import plot_technical_indicators

# Import agents for analysis
from agents import finance_news_analyst, \
    finance_data_analyst, technical_data_analyst, \
    head_analyst, summerize_agent

# Import function to merge markdown files
from modules.past_market_intel import merge_markdown_files

# Load the environment variables
load_dotenv()

def run_main():
    """
    Main function to run the Bitcoin analysis pipeline.

    This function performs the following steps:
    1. Defines constants for the asset, ticker symbol, and language model.
    2. Initializes the language model using the OpenAI API.
    3. Scrapes news headlines related to Bitcoin.
    4. Downloads financial data from Yahoo Finance.
    5. Scrapes technical data.
    6. Plots financial and technical indicators.
    7. Analyzes news headlines using a financial news analyst agent.
    8. Analyzes financial data using a financial data analyst agent.
    9. Analyzes technical data using a technical data analyst agent.
    10. Loads previous reports for historical analysis.
    11. Uses a head analyst agent to analyze the results of the other agents.
    12. Summarizes the results from the head analyst.
    13. Saves the final report to a markdown file.
    14. Merges the most recent reports into a single markdown file.
    15. Prints the results of the analysis.

    Returns:
        None
    """

    # Define constants
    ASSET = "bitcoin"
    TICKER_SYMBOL = "BTC-USD"
    MODEL = "o1-preview"
    #MODEL = "gpt-3.5-turbo"

    # Initialize the language model
    llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model=MODEL)

    # Scrape news headlines
    all_headlines = scrape(url="https://news.google.com/search?q=bitcoin&hl=en-US&gl=US&ceid=US%3Aen")

    # Scrape yfinance data
    data = download_yfinance_data(
        ticker_symbol=TICKER_SYMBOL,
        start_date=datetime.now() - timedelta(days=365),
        asset=ASSET,
        end_date=datetime.now()
    )

    # Scrape technical data
    data_tech = get_data(print_data=False)

    # Plot financial data
    plot_technical_indicators(data=data, data_tech=data_tech)

    # Use financial news analyst agent to analyze news
    output_news_analyst = finance_news_analyst(
        prompt_path="src/prompts/news_analyst.md",
        all_headlines=all_headlines,
        llm=llm
    )

    # Use financial data analyst agent to analyze financial data
    output_finance_analyst = finance_data_analyst(
        prompt_path="src/prompts/financial_analyst.md",
        data=data,
        asset=ASSET,
        llm=llm
    )

    # Use technical data analyst agent to analyze technical data
    output_technical_analyst = technical_data_analyst(
        prompt_path="src/prompts/technical_analyst.md",
        data=data_tech,
        asset=ASSET,
        llm=llm
    )

    # Load the previous reports
    with open('reports/merged_report.md', 'r', encoding='utf-8') as file:
        historical_data = file.read()

    # Use head analyst agent to analyze the results of the other agents
    output_head_analyst = head_analyst(
        prompt_path="src/prompts/head_analyst.md",
        result_1=output_news_analyst,
        result_2=output_finance_analyst,
        result_3=output_technical_analyst,
        llm=llm,
        date=datetime.now().strftime('%Y-%m-%d %H'),
        historical_data=historical_data,
        print_prompt=False
    )

    # Summarize the results from the head analyst
    summary_results_head_analyst = summerize_agent(
        prompt_path="src/prompts/summarizer.md",
        data=output_head_analyst,
        llm=llm
    )

    # Save the final report
    report = f"report-{datetime.now():%Y-%m-%d}.md"
    save_path = os.path.join('reports', report)
    os.makedirs('reports', exist_ok=True)
    with open(save_path, "w") as file:
        file.write(summary_results_head_analyst)

    # Merge the most recent reports
    merge_markdown_files(
        directory='reports',
        num_files=7,
        output_file='reports/merged_report.md'
    )

    # Print results
    tasks = [
        ("News Analyst", output_news_analyst),
        ("Finance Analyst", output_finance_analyst),
        ("Technical Analyst", output_technical_analyst),
        ("Head Analyst", output_head_analyst)
    ]

    for agent, output in tasks:
        print(f"\n === {agent} === \n\n{output}\n")



result = subprocess.run([sys.executable, "-m", "pytest", "scraper/test_yfinance_scraper.py"], capture_output=True, text=True)
print(result.stdout)

# Stop execution if tests fail
if result.returncode != 0:
    print("Unit tests failed. Exiting...")
    sys.exit(1)







if __name__ == "__main__":
    run_main()