# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/data_loader.py
# Назначение: Загрузка исторических данных с Binance
# ============================================

import pandas as pd
from binance.client import Client
from bot_ai.config.config_loader import get_binance_credentials

# Инициализация клиента
api_key, api_secret = get_binance_credentials()
client = Client(api_key, api_secret)

def load_data(symbol: str, interval: str, limit: int = 100) -> pd.DataFrame:
    """
    Загружает исторические свечи с Binance и возвращает DataFrame.
    """
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        df = df.astype({
            "open": "float",
            "high": "float",
            "low": "float",
            "close": "float",
            "volume": "float"
        })
        return df

    except Exception as e:
        print(f"❌ Ошибка при загрузке данных для {symbol}: {e}")
        return pd.DataFrame()
