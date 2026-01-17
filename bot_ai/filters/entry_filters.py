# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/filters/entry_filters.py
# Назначение: Фильтры входа по волатильности (ATR) и тренду (ADX)
# ============================================

import logging

import pandas as pd

def atr_filter(df: pd.DataFrame, period=14, threshold=0.01):
    if len(df) < period + 1:
        return False

    high = df["high"]
    low = df["low"]
    close = df["close"]

    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = tr.rolling(window=period).mean().iloc[-1]
    price = close.iloc[-1]
    atr_pct = atr / price

    if atr_pct < threshold:
        logging.info(
            f"[FILTER:volatility] ? ATR {
                atr_pct:.4f} < threshold {threshold}")
        return False

    logging.info(
        f"[FILTER:volatility] ? ATR {
            atr_pct:.4f} >= threshold {threshold}")
    return True

def adx_filter(df: pd.DataFrame, period=14, threshold=20):
    if len(df) < period * 2:
        return False

    high = df["high"]
    low = df["low"]
    close = df["close"]

    plus_dm = high.diff()
    minus_dm = low.diff().abs()

    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm < 0] = 0

    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = tr.rolling(window=period).mean()
    plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr)
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.rolling(window=period).mean().iloc[-1]

    if adx < threshold:
        logging.info(f"[FILTER:trend] ? ADX {adx:.2f} < threshold {threshold}")
        return False

    logging.info(f"[FILTER:trend] ? ADX {adx:.2f} >= threshold {threshold}")
    return True

