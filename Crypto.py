import requests
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# 1. Setup Argument Parsing
parser = argparse.ArgumentParser(description='Fetch and plot Cryptocurrency prices.')
parser.add_argument('--item', type=str, default='BTC', 
                    help='Crypto symbol (e.g., BTC, ETH, SOL)')
parser.add_argument('--time', type=str, default='6m', 
                    choices=['1m', '2m', '3m', '6m', '1y', '2y', '5y', '10y'], 
                    help='Time range to plot')

args = parser.parse_args()

# Map the --time argument to Pandas DateOffset
time_map = {
    '1m': {'months': 1}, '2m': {'months': 2}, '3m': {'months': 3}, '6m': {'months': 6},
    '1y': {'years': 1}, '2y': {'years': 2}, '5y': {'years': 5}, '10y': {'years': 10}
}

symbol = args.item.upper()
key = "DVA9SPFTK0SCT9NO"

# 2. Fetch Data
# Note: Market is set to USD as per your requirement
url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market=USD&apikey=demo'
response = requests.get(url)
json_data = response.json()

# The crypto API uses a different key for its time series data
data_key = "Time Series (Digital Currency Daily)"

if data_key in json_data:
    # 3. Parse and Clean Data
    # We transpose (.T) because the JSON is oriented by date keys
    df = pd.DataFrame(json_data[data_key]).T
    
    # Reset index to turn the date string into a column
    df = df.reset_index()
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    
    # Convert types
    df['date'] = pd.to_datetime(df['date'])
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df = df.dropna(subset=['close'])
    
    # 4. Filter based on --time
    latest_date = df['date'].max()
    offset_params = time_map[args.time]
    start_date = latest_date - pd.DateOffset(**offset_params)
    
    df_filtered = df[df['date'] >= start_date].sort_values('date')
    
    # 5. Visualization
    plt.figure(figsize=(12, 6))
    plt.plot(df_filtered['date'], df_filtered['close'], color='#f39c12', linewidth=2, label=f"{symbol}/USD")
    
    
    
    plt.title(f"{symbol} Price - Last {args.time}\nEnding {latest_date.strftime('%Y-%m-%d')}")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 6. Save and Show
    filename = f'crypto_{symbol.lower()}_{args.time}.png'
    plt.savefig(filename)
    plt.show()
    
    print(f"Successfully plotted {len(df_filtered)} days of data for {symbol}.")
else:
    # Handle API errors or rate limits
    error_msg = json_data.get("Error Message", json_data.get("Note", "Unknown Error"))
    print