import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import argparse

# 1. Setup Argument Parsing
parser = argparse.ArgumentParser(description='Fetch and plot Crude Oil prices (Brent or WTI).')
parser.add_argument('--item', type=str, default='brent', 
                    choices=['brent', 'wti'],
                    help='Oil type: brent or wti')
parser.add_argument('--interval', type=str, default='daily', 
                    choices=['daily', 'weekly', 'monthly'], 
                    help='Data interval: daily, weekly, or monthly')
parser.add_argument('--time', type=str, default='6m', 
                    choices=['1m', '2m', '3m', '6m', '1y', '2y', '5y', '10y'], 
                    help='Time range to plot')

args = parser.parse_args()

# Map the --time argument to Pandas DateOffset
time_map = {
    '1m': {'months': 1}, '2m': {'months': 2}, '3m': {'months': 3}, '6m': {'months': 6},
    '1y': {'years': 1}, '2y': {'years': 2}, '5y': {'years': 5}, '10y': {'years': 10}
}

interval = args.interval.lower()
b_or_w = args.item.upper()
key = "DVA9SPFTK0SCT9NO"

# 2. Fetch Data
url = f'https://www.alphavantage.co/query?function={b_or_w}&interval={interval}&apikey={key}'
response = requests.get(url)
json_data = response.json()

if "data" in json_data:
    df = pd.DataFrame(json_data['data'])
    
    # Clean data
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df['date'] = pd.to_datetime(df['date'])
    df = df.dropna(subset=['value'])
    
    # 3. Filter based on --time
    latest_date = df['date'].max()
    offset_params = time_map[args.time]
    start_date = latest_date - pd.DateOffset(**offset_params)
    
    df_filtered = df[df['date'] >= start_date].sort_values('date')
    
    # 4. Visualization
    plt.figure(figsize=(12, 6))
    
    # Plotting
    plt.plot(df_filtered['date'], df_filtered['value'], color='#2c3e50', linewidth=2, label=b_or_w)
    
    
    
    # Titles and Labels
    plt.title(f"{b_or_w} ({interval.capitalize()}) - Last {args.time}\nEnding {latest_date.strftime('%Y-%m-%d')}")
    plt.xlabel("Date")
    plt.ylabel("Price (USD per Barrel)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 5. Save and Show
    filename = f'{b_or_w.lower()}_{interval}_{args.time}.png'
    plt.savefig(filename)
    plt.show()
    
    print(f"Successfully plotted {len(df_filtered)} data points for {b_or_w}.")
else:
    print(f"Error: API failed for {b_or_w}. Check key or connection.")