import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_technical_indicators(data: pd.DataFrame) -> None:

    data.reset_index(inplace=True)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Calculating 20-day and 50-day moving averages
    data['20_MA'] = data['Close'].rolling(window=20).mean()
    data['50_MA'] = data['Close'].rolling(window=50).mean()

    # Creating the plot
    plt.figure(figsize=(10, 6))

    # Plotting close price with 20-day and 50-day moving averages
    plt.subplot(2, 1, 1)
    plt.plot(data.index, data['Close'], label='Close Price', marker='.')
    plt.plot(data.index, data['20_MA'], label='20 Day MA', linestyle='--', color='orange')
    plt.plot(data.index, data['50_MA'], label='50 Day MA', linestyle='--', color='green')
    plt.title('Close Price with 20 and 50 Day Moving Averages')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.legend()

    # Plotting MACD and MACD Histogram
    plt.subplot(2, 1, 2)
    plt.plot(data.index, data['MACD'], label='MACD', marker='.')
    plt.plot(data.index, data['Signal_Line'], label='Signal Line', marker='.', linestyle='--')
    plt.bar(data.index, data['MACD_Histogram'], label='MACD Histogram', alpha=0.5)
    plt.title('MACD Analysis')
    plt.ylabel('MACD Value')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    save_path = os.path.join('images', 'finance_plot.png')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    try:
        plt.savefig(save_path)
        print(f"File saved successfully at {save_path}")
    except Exception as e:
        print(f"An error occurred: {e}")