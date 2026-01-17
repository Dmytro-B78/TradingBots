# -*- coding: utf-8 -*-
# ============================================
# File: indicators.py
# Назначение: Индикаторы SMA, ATR, ADX
# ============================================

import pandas as pd

def calculate_sma(series: pd.Series, period: int) -> pd.Series:
    """
    Простая скользящая средняя (SMA)
    """
    return series.rolling(window=period).mean()

def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Средний истинный диапазон (ATR)
    """
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

def calculate_adx(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Упрощённый ADX (без сглаживания)
    """
    up_move = df["high"].diff()
    down_move = df["low"].diff().abs()
    tr = df["high"].combine(df["low"], max) - df["low"].combine(df["close"].shift(), min)
    dx = (up_move - down_move).abs() / tr.replace(0, 1)
    adx = dx.rolling(window=period).mean()
    return adx
