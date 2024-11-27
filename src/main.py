import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load the environment variables
load_dotenv()

import argparse

parser = argparse.ArgumentParser(description="Bitcoin trader")

parser.add_argument("--test_run", "-n", type=str, default="False", help="Run in test or production mode")
args = parser.parse_args()


def run_main(args):
    # ----------------- PARAMETERS -----------------
    TEST_RUN = args.test_run

    ASSET = "bitcoin"
    if ASSET == "bitcoin":
        TICKER_SYMBOL = "BTC-USD"

    from langchain_openai import ChatOpenAI

    if TEST_RUN=="True":
        model = "gpt-4o"
        print(f"\n\n\nTHIS IS A TEST RUN! - {model}\n\n\n")
        llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model=model)
    else:
        model = "gpt-4-turbo"
        print(f"\n\n\nTHIS IS A PRODUCTION RUN - {datetime.now():%Y-%m-%d} - {model}\n\n\n")
        llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model=model)

    # ----------------- Scrape news headlines -----------------
    from scraper.googlenews import scrape
    all_headlines = scrape(url="https://news.google.com/search?q=bitcoin&hl=en-US&gl=US&ceid=US%3Aen")

    # ----------------- Analyze content -----------------
    from agents import finance_news_analyst
    prompt = "src/prompts/news_analyst.md"
    output_news_analyst = finance_news_analyst(prompt, all_headlines, llm)
    print(f"\n\n\n\n ======= News analyst ======= \n\n{output_news_analyst}\n\n\n\n")

    # ----------------- Scrape financial data -----------------
    from scraper.yfinance import download_yfinance_data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    data = download_yfinance_data(ticker_symbol=TICKER_SYMBOL, start_date=start_date,
                                end_date=end_date, asset=ASSET, print_data=True)

    # ----------------- Scrape technical data -----------------
    from scraper.bitcoin_tech import get_data
    data_tech = get_data(print_data=True)

    # ----------------- Plot financial data -----------------
    from helper.plotter import plot_technical_indicators
    plot_technical_indicators(data=data, data_tech=data_tech)

    # ----------------- Analyze financial data -----------------
    from agents import finance_data_analyst
    prompt = "src/prompts/financial_analyst.md"
    output_finance_analyst = finance_data_analyst(prompt=prompt, data=data, asset=ASSET, llm=llm)
    print(f"\n\n\n\n ======= Financial analyst ======= \n\n{output_finance_analyst}\n\n\n\n")

    # ----------------- Analyze technical data -----------------
    from agents import technical_data_analyst
    prompt = "src/prompts/technical_analyst.md"
    output_technical_analyst = technical_data_analyst(prompt=prompt, data=data_tech, asset=ASSET, llm=llm)
    print(f"\n\n\n\n ======= Technical analyst ======= \n\n{output_technical_analyst}\n\n\n\n")

    # ----------------- Analyze technical bitcoin data -----------------
    from scraper.bitcoin_tech import get_data
    bitcoin_data = get_data()

    # ----------------- Head analyst -----------------
    from agents import head_analyst
    date_time = datetime.now().strftime('%Y-%m-%d %H')
    prompt = "src/prompts/head_analyst.md"
    output_head_analyst = head_analyst(prompt=prompt,
                            result_1=output_news_analyst,
                            result_2=output_finance_analyst,
                            result_3=output_technical_analyst,
                            llm=llm,
                            date=date_time)

    print(f"\n\n\n\n ======= Head analyst ======= \n\n{output_head_analyst}\n\n\n\n")


    # ----------------- Save report -----------------

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