import requests
import json
import os
import time
from datetime import datetime, timedelta

historical_url = "https://api.coingecko.com/api/v3/coins/{}/market_chart"
crypto_ids = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "tether": "USDT",
    "usd-coin": "USDC",
    "binancecoin": "BNB",
    "ripple": "XRP",
    "cardano": "ADA",
    "binance-usd": "BUSD"
}

save_directory = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

file_name = os.path.join(save_directory, "cryptos_historical_data.json")

def get_historical_data(crypto_id):
    days = "365" 
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }

    response = requests.get(historical_url.format(crypto_id), params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        
        return None


historical_data = {}

for crypto_id, symbol in crypto_ids.items():
    print(f"Fetching data for {symbol} ({crypto_id})...")
    data = get_historical_data(crypto_id)
    if data:
        historical_data[symbol] = data
    time.sleep(3)  

with open(file_name, 'w') as file:
    json.dump(historical_data, file, indent=4)


