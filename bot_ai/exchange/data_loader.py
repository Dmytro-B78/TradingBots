# data_loader.py
# Назначение: Загрузка OHLCV‑данных с биржи (через CCXT)
# Структура:
# └── bot_ai/exchange/data_loader.py

import ccxt
import pandas as pd

def load_ohlcv(symbol, timeframe="1h", limit=500):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df
