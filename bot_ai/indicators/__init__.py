# ============================================
# Path: C:\TradingBots\NT\bot_ai\indicators\__init__.py
# Purpose: Technical indicator functions for strategies
# Format: UTF-8 without BOM, production-ready
# ============================================

import pandas as pd

def calculate_sma(series: pd.Series, period: int) -> pd.Series:
    """Simple Moving Average (SMA) over a given period."""
    return series.rolling(window=period).mean()

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Relative Strength Index (RSI) over a given period."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    """MACD line, signal line, and histogram."""
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_std(series: pd.Series, period: int) -> pd.Series:
    """Rolling standard deviation over a given period."""
    return series.rolling(window=period).std()

def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average True Range (ATR) over a given period."""
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr
