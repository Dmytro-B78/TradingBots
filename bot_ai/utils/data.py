# ============================================
# File: bot_ai/utils/data.py
# Purpose: Load OHLCV data from Binance spot (live only)
# Encoding: UTF-8
# ============================================

import pandas as pd
import os
import ccxt

def fetch_ohlcv(symbol, timeframe="1h", limit=1000):
    """
    Loads OHLCV data from local CSV if available, otherwise fetches from Binance spot API (live).
    """
    filename = f"data/{symbol.replace('/', '')}_{timeframe}.csv"
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename, parse_dates=["time"])
            df = df.tail(limit).copy()
            df.reset_index(drop=True, inplace=True)
            return df
        except Exception as e:
            print(f"[ERROR] Failed to read CSV file {filename}: {e}")
            return None

    try:
        exchange = ccxt.binance({
            "enableRateLimit": True,
            "options": {
                "defaultType": "spot"
            }
        })

        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["time", "open", "high", "low", "close", "volume"])
        df["time"] = pd.to_datetime(df["time"], unit="ms")

        os.makedirs("data", exist_ok=True)
        df.to_csv(filename, index=False, encoding="utf-8")
        return df

    except Exception as e:
        print(f"[ERROR] Failed to fetch OHLCV from Binance for {symbol}: {e}")
        return None
