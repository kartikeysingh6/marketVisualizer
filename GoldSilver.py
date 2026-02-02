import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import argparse
import sys

# 1. Setup Argument Parsing
parser = argparse.ArgumentParser(description='Fetch and plot precious metal prices.')
parser.add_argument('--item', type=str, default='gold', choices=['gold', 'silver'], 
                    help='Item to fetch: gold or silver')
parser.add_argument('--interval', type=str, default='daily', choices=['daily', 'weekly', 'monthly'], 
                    help='Data interval: daily, weekly, or monthly')
parser.add_argument('--time', type=str, default='6m', 
                    choices=['1m', '2m', '3m', '6m', '1y', '2y', '5y', '10y'], 
                    help='Time range to plot (e.g., 6m, 1y, 5y)')

args = parser.parse_args()

# Map the --time argument to Pandas DateOffset parameters
time_map = {
    '1m': {'months': 1}, '2m': {'months': 2}, '3m': {'months': 3}, '6m': {'months': 6},
    '1y': {'years': 1}, '2y': {'years': 2}, '5y': {'years': 5}, '10y': {'years': 10}
}

g_or_s = args.item.upper()
interval = args.interval.lower()
key = "DVA9SPFTK0SCT9NO"

# 2. Fetch Data
url = f'https://www.alphavantage.co/query?function=GOLD_SILVER_HISTORY&symbol={g_or_s}&interval={interval}&apikey={key}'
response = requests.get(url)
json_data = response.json()

if "data" in json_data:
    df = pd.DataFrame(json_data['data'])
    df['date'] = pd.to_datetime(df['date'])
    df['price'] = pd.to_numeric(df['price'])
    
    # 3. Filter based on --time argument
    latest_date = df['date'].max()
    offset_params = time_map[args.time]
    start_date = latest_date - pd.DateOffset(**offset_params)
    
    df_filtered = df[df['date'] >= start_date].sort_values('date')
    
    # 4. Visualization
    plt.figure(figsize=(12, 6))
    
    if g_or_s == "SILVER":
        color, label, y_label = '#C0C0C0', 'Silver Price', 'Price $/kg'
    else:
        color, label, y_label = '#D4AF37', 'Gold Price', 'Price $/10g'
    
    plt.plot(df_filtered['date'], df_filtered['price'], color=color, linewidth=2, label=label)
    
    # Titles and Labels
    plt.title(f"{g_or_s} ({interval.capitalize()}) - Last {args.time}\nEnding {latest_date.strftime('%Y-%m-%d')}")
    plt.xlabel("Date")
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 5. Output
    filename = f'{g_or_s}_{interval}_{args.time}.png'
    plt.savefig(filename)
    plt.show()
    
    print(f"Successfully plotted {len(df_filtered)} points for {g_or_s} ({args.time}).")
    print(f"Saved as: {filename}")
else:
    print(f"Error: API returned no data for {g_or_s}. Check your API key or interval settings.")