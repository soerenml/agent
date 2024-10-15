import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_technical_indicators(data: pd.DataFrame) -> None:
    # Plotting
    plt.figure(figsize=(12, 8))

    # Close price
    plt.plot(data.index, data['Close'], label='Close Price', color='blue')

    # Moving Averages (MA)
    data['50-Day MA'] = data['Close'].rolling(window=50).mean()
    data['200-Day MA'] = data['Close'].rolling(window=200).mean()
    plt.plot(data.index, data['50-Day MA'], label='50-Day MA', color='orange')
    plt.plot(data.index, data['200-Day MA'], label='200-Day MA', color='green')

    # Relative Strength Index (RSI)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    plt.plot(data.index, rsi, label='RSI', color='purple')

    # Moving Average Convergence Divergence (MACD)
    ema_12 = data['Close'].ewm(span=12, min_periods=12).mean()
    ema_26 = data['Close'].ewm(span=26, min_periods=26).mean()
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9, min_periods=9).mean()
    plt.plot(data.index, macd, label='MACD', color='red')
    plt.plot(data.index, signal, label='MACD Signal', color='cyan')

    plt.title('Dell Technologies Inc. Stock Price & Technical Indicators Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price / Indicator Value')
    plt.legend()
    plt.grid(True)

    save_path = os.path.join('images', 'finance_plot.png')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)