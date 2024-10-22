import datetime
import typing
import requests
from random import choice
import pandas as pd

# URL of the Fear & Greed Index API
URL = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"

# User agents for rotating requests (optional, for evading simple bot detection)
USER_AGENTS = [
    # Chrome on Windows 10
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
    # Chrome on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
    # Chrome on Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
    # Firefox on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
    # Firefox on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.4; rv:100.0) Gecko/20100101 Firefox/100.0",
]
def get_data():
    user_agent = choice(USER_AGENTS)  # Choose a random user agent
    headers = {
        "User-Agent": user_agent,
    }
    r = requests.get(URL, headers=headers)
    df = pd.json_normalize(r)
    #df = pd.DataFrame(r.json())
    r.raise_for_status()
    return df

import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_technical_indicators(data: pd.DataFrame) -> None:

    data.reset_index(inplace=True)
    data['Date'] = pd.to_datetime(data['timestamp'])
    data.set_index('Date', inplace=True)

    # Calculating 20-day and 50-day moving averages
    data['20_fg'] = data['score'].rolling(window=20).mean()
    data['50_fg'] = data['score'].rolling(window=50).mean()

    # Creating the plot
    plt.figure(figsize=(10, 6))

    # Plotting close price with 20-day and 50-day moving averages
    plt.subplot(2, 1, 1)
    plt.plot(data.index, data['Score'], label='score', marker='.')
    plt.plot(data.index, data['20_fg'], label='20 Day FG', linestyle='--', color='orange')
    plt.plot(data.index, data['20_fg'], label='50 Day FG', linestyle='--', color='green')
    plt.title('Close Price with 20 and 50 Day Moving Averages')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    save_path = os.path.join('images', 'fg_plot.png')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    try:
        plt.savefig(save_path)
        print(f"File saved successfully at {save_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
fg = get_data()
print(fg)
#plot_technical_indicators(fg['fear_and_greed'])