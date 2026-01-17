# bot_ai/strategy/countertrend.py
# Контртрендовая стратегия: RSI экстремумы

from bot_ai.utils.data import fetch_ohlcv
from bot_ai.utils.indicators import rsi

def run(pair, timeframe):
    df = fetch_ohlcv(pair, timeframe=timeframe)
    if df is None or df.empty:
        return None

    df["rsi"] = rsi(df["close"], 14)

    if df["rsi"].iloc[-1] > 80:
        return "sell"
    elif df["rsi"].iloc[-1] < 20:
        return "buy"
    return None

