# bot_ai/utils/indicators.py
# Индикаторы: EMA, SMA, RSI, ATR

import numpy as np
import pandas as pd

def sma(series, period):
    """
    Простое скользящее среднее (Simple Moving Average)
    """
    return series.rolling(window=period).mean()

def ema(series, period):
    """
    Экспоненциальное скользящее среднее (Exponential Moving Average)
    """
    return series.ewm(span=period, adjust=False).mean()

def rsi(series, period=14):
    """
    Индекс относительной силы (Relative Strength Index)
    """
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def atr(df, period=14):
    """
    Средний истинный диапазон (Average True Range)
    """
    high_low = df["high"] - df["low"]
    high_close = np.abs(df["high"] - df["close"].shift())
    low_close = np.abs(df["low"] - df["close"].shift())

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

