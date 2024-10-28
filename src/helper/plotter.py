import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_technical_indicators(data: pd.DataFrame, data_tech: pd.DataFrame) -> None:

    data.reset_index(inplace=True)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Calculating 20-day and 50-day moving averages
    data['20_MA'] = data['Close'].rolling(window=20).mean()
    data['50_MA'] = data['Close'].rolling(window=50).mean()

    # Creating the plot with extra height for more subplots
    plt.figure(figsize=(12, 18))  # Increased figure size for additional subplots

    # Plotting close price with 20-day and 50-day moving averages
    plt.subplot(6, 1, 1)
    plt.plot(data.index, data['Close'], label='Close Price', marker='.')
    plt.plot(data.index, data['20_MA'], label='20 Day MA', linestyle='--', color='orange')
    plt.plot(data.index, data['50_MA'], label='50 Day MA', linestyle='--', color='green')
    plt.title('Close Price with 20 and 50 Day Moving Averages')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.legend()

    # Plotting MACD and MACD Histogram
    plt.subplot(6, 1, 2)
    plt.plot(data.index, data['MACD'], label='MACD', marker='.')
    plt.plot(data.index, data['Signal_Line'], label='Signal Line', marker='.', linestyle='--')
    plt.bar(data.index, data['MACD_Histogram'], label='MACD Histogram', alpha=0.5)
    plt.title('MACD Analysis')
    plt.ylabel('MACD Value')
    plt.grid(True)
    plt.legend()

    # Plotting RSI with horizontal lines at 70 and 30
    plt.subplot(6, 1, 3)
    plt.plot(data.index, data['relative_strength_index_RSI'], label='RSI', marker='.')
    plt.axhline(70, color='red', linestyle='--', linewidth=0.8, label='Overbought (70)')
    plt.axhline(30, color='green', linestyle='--', linewidth=0.8, label='Oversold (30)')
    plt.title('RSI Analysis')
    plt.ylabel('RSI Value')
    plt.grid(True)
    plt.legend()

    # Plotting Hash Rate and moving averages from data_tech
    plt.subplot(6, 1, 4)
    plt.plot(data_tech['Timestamp'], data_tech['hash_rate'], label='Hash Rate', marker='.')
    plt.plot(data_tech['Timestamp'], data_tech['hash_rate-9-day'], label='9 Day MA', linestyle='--')
    plt.plot(data_tech['Timestamp'], data_tech['hash_rate-14-day'], label='14 Day MA', linestyle='--')
    plt.plot(data_tech['Timestamp'], data_tech['hash_rate-25-day'], label='25 Day MA', linestyle='--')
    plt.title('Hash Rate Analysis')
    plt.ylabel('Hash Rate')
    plt.grid(True)
    plt.legend()

    # Plotting Difficulty Ribbon and its moving averages from data_tech
    plt.subplot(6, 1, 5)
    plt.plot(data_tech['Timestamp'], data_tech['difficulty_ribbon'], label='Difficulty Ribbon', marker='.')
    plt.plot(data_tech['Timestamp'], data_tech['difficulty_ribbon-9-day'], label='9 Day MA', linestyle='--')
    plt.plot(data_tech['Timestamp'], data_tech['difficulty_ribbon-14-day'], label='14 Day MA', linestyle='--')
    plt.plot(data_tech['Timestamp'], data_tech['difficulty_ribbon-25-day'], label='25 Day MA', linestyle='--')
    plt.title('Difficulty Ribbon Analysis')
    plt.ylabel('Difficulty Ribbon')
    plt.grid(True)
    plt.legend()

    # Plotting Active Addresses and its moving averages from data_tech
    plt.subplot(6, 1, 6)
    plt.plot(data_tech['Timestamp'], data_tech['active_addresses'], label='Active Addresses', marker='.')
    plt.plot(data_tech['Timestamp'], data_tech['active_addresses-9-day'], label='9 Day MA', linestyle='--')
    plt.plot(data_tech['Timestamp'], data_tech['active_addresses-14-day'], label='14 Day MA', linestyle='--')
    plt.plot(data_tech['Timestamp'], data_tech['active_addresses-25-day'], label='25 Day MA', linestyle='--')
    plt.title('Active Addresses Analysis')
    plt.ylabel('Active Addresses')
    plt.grid(True)
    plt.legend()

    # Automatically adjust spacing
    plt.tight_layout()

    # Save the plot
    save_path = os.path.join('images', 'finance_plot.png')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    try:
        plt.savefig(save_path)
        print(f"File saved successfully at {save_path}")
    except Exception as e:
        print(f"An error occurred: {e}")