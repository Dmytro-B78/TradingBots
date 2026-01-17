# -*- coding: utf-8 -*-
# === bot_ai/utils/data.py ===
# Загрузка OHLCV-данных с Binance через API с логированием

import logging

import pandas as pd
import requests

# === Загрузка исторических свечей с Binance ===

def fetch_ohlcv(
        symbol: str,
        interval: str = "15m",
        limit: int = 200) -> pd.DataFrame:
    """
    Загружает исторические свечи OHLCV с Binance API.
    :param symbol: Тикер (например, "BTCUSDT")
    :param interval: Таймфрейм (например, "15m", "1h", "1d")
    :param limit: Кол-во свечей (макс. 1000)
    :return: DataFrame с колонками: time, open, high, low, close, volume
    """
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit
    }

    logging.info(
        f"[DATA] ?? Запрос данных: symbol={symbol}, interval={interval}, limit={limit}")

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        raw = response.json()

        df = pd.DataFrame(raw, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
        ])

        df = df[["open_time", "open", "high", "low", "close", "volume"]].copy()
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
        df.set_index("open_time", inplace=True)
        df = df.astype(float)

        logging.info(f"[DATA] ? Загружено {len(df)} свечей для {symbol}")
        return df

    except Exception as e:
        logging.error(f"[DATA] ? Ошибка загрузки данных: {e}")
        return pd.DataFrame()

def load_ohlcv(symbol: str, timeframe: str, days: int) -> pd.DataFrame:
    """
    Обёртка над fetch_ohlcv для совместимости с движком бэктеста.
    days → limit (примерно 24 * days свечей на 1h)
    """
    candles_per_day = {
        "1m": 1440, "5m": 288, "15m": 96, "30m": 48,
        "1h": 24, "4h": 6, "1d": 1
    }
    per_day = candles_per_day.get(timeframe, 24)
    limit = min(days * per_day, 1000)  # Binance ограничивает до 1000

    return fetch_ohlcv(symbol, interval=timeframe, limit=limit)
