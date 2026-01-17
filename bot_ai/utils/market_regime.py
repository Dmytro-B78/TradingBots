# ============================================
# 🧠 market_regime.py — Классификация рынка
# --------------------------------------------
# Возвращает: "trend", "flat", "volatile"
# ============================================

import pandas as pd
import numpy as np

def compute_adx(df, period=14):
    high = df["high"]
    low = df["low"]
    close = df["close"]

    plus_dm = high.diff()
    minus_dm = low.diff().abs()

    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm < 0] = 0

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = tr.rolling(window=period).mean()
    plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr)
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    adx = dx.rolling(window=period).mean()

    return adx

def detect_market_regime(df):
    adx = compute_adx(df)
    volatility = df["close"].pct_change().rolling(14).std()

    latest_adx = adx.iloc[-1]
    latest_vol = volatility.iloc[-1]

    if latest_adx > 25:
        return "trend"
    elif latest_vol > 0.02:
        return "volatile"
    else:
        return "flat"
