# ============================================
# File: download_binance.py
# Purpose: Download historical candlestick data from Binance
# Source: https://api.binance.com/api/v3/klines
# Loads symbols from data/whitelist.json
# Saves to data/history/<SYMBOL>_<TIMEFRAME>.csv
# ============================================

import os
import json
import time
import requests
import pandas as pd
from datetime import datetime, timedelta

# === Settings ===
TIMEFRAMES = ["1h", "15m"]
DAYS_BACK = 90
OUTPUT_DIR = "data/history"
WHITELIST_PATH = "data/whitelist.json"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Binance REST API ===
BASE_URL = "https://api.binance.com/api/v3/klines"
LIMIT = 1000

def load_whitelist():
    with open(WHITELIST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def download_klines(symbol, interval, start_time_ms, end_time_ms):
    all_klines = []
    while start_time_ms < end_time_ms:
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_time_ms,
            "endTime": end_time_ms,
            "limit": LIMIT
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            print(f"❌ Error {symbol} [{interval}]: {response.status_code} {response.text}")
            break

        data = response.json()
        if not data:
            break

        all_klines.extend(data)
        last_time = data[-1][0]
        start_time_ms = last_time + 1
        time.sleep(0.2)
    return all_klines

def save_klines(symbol, klines, interval):
    df = pd.DataFrame(klines, columns=[
        "time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df = df[["time", "open", "high", "low", "close", "volume"]]
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)

    out_path = os.path.join(OUTPUT_DIR, f"{symbol}_{interval}.csv")
    df.to_csv(out_path, index=False)
    print(f"✅ Saved: {out_path}")

def main():
    entries = load_whitelist()
    end_time = int(time.time() * 1000)
    start_time = int((datetime.utcnow() - timedelta(days=DAYS_BACK)).timestamp() * 1000)

    for entry in entries:
        symbol = entry["symbol"]
        for interval in TIMEFRAMES:
            try:
                print(f"⬇️ Downloading: {symbol} | {interval}")
                klines = download_klines(symbol, interval, start_time, end_time)
                if klines:
                    save_klines(symbol, klines, interval)
                else:
                    print(f"⚠️ No data for {symbol} [{interval}]")
            except Exception as e:
                print(f"❌ Error {symbol} [{interval}]: {e}")

if __name__ == "__main__":
    main()
