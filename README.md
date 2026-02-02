# 📈 Market Tracker CLI

![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)

A lightweight command-line suite to fetch, analyze, and visualize global market trends for **Crude Oil** and **Cryptocurrencies** using the Alpha Vantage API.

## 🚀 Overview

This project consists of two specialized scripts designed for rapid market analysis:
- `oil.py`: Tracks Brent and WTI crude oil prices (Daily/Weekly/Monthly).
- `crypto.py`: Tracks digital currency (BTC, ETH, etc.) performance against USD.



## ✨ Key Features

* **Custom Timeframes**: Support for `1m`, `3m`, `6m`, `1y`, `5y`, and even `10y` views.
* **Automatic Visualization**: Generates high-resolution PNG charts automatically.
* **Robust Data Cleaning**: Handles missing values and API "nulls" gracefully.
* **Secure**: Zero hardcoded API keys. Uses system environment variables for security.
* **Smart Error Handling**: Detects and reports API rate limits or invalid symbols.

## 🛠️ Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/market-tracker.git](https://github.com/yourusername/market-tracker.git)
    cd market-tracker
    ```

2.  **Install dependencies:**
    ```bash
    pip install requests pandas matplotlib
    ```

3.  **Configure API Key:**
    Get your free key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key) and export it:
    ```bash
    # macOS/Linux
    export ALPHA_VANTAGE_KEY="your_key_here"
    
    # Windows (PowerShell)
    $env:ALPHA_VANTAGE_KEY = "your_key_here"
    ```

## 📖 Usage Examples

### 🛢️ Crude Oil Analysis
Fetch the last 6 months of Brent Crude data on a daily interval:
```bash
python3 oil.py --item brent --interval daily --time 6m
