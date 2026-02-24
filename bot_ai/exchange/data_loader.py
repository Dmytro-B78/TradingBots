# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/exchange/data_loader.py
# Purpose: Load OHLCV data from exchange and standardize column names
# ============================================

import ccxt
import pandas as pd

def load_ohlcv(symbol, timeframe="1h", limit=500):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["time"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df.drop(columns=["timestamp"])
    df = df[["time", "open", "high", "low", "close", "volume"]]
    return df
