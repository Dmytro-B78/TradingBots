# bot_ai/strategy/breakout.py
# Пробой диапазона: high/low за 20 баров

from bot_ai.utils.data import fetch_ohlcv

def run(pair, timeframe):
    df = fetch_ohlcv(pair, timeframe=timeframe)
    if df is None or df.empty:
        return None

    high = df["high"].rolling(20).max()
    low = df["low"].rolling(20).min()
    close = df["close"]

    if close.iloc[-1] > high.iloc[-2]:
        return "buy"
    elif close.iloc[-1] < low.iloc[-2]:
        return "sell"
    return None

