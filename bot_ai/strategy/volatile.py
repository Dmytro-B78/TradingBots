# ============================================
# File: bot_ai/strategy/volatile.py
# Purpose: Volatility breakout strategy using standard deviation
# Compatible with BaseStrategy, MarketContext, Signal
# ============================================

import pandas as pd
from bot_ai.strategy.base_strategy import BaseStrategy
from bot_ai.core.signal import Signal

class VolatileStrategy(BaseStrategy):
    def __init__(self, config):
        self.window = config.get("window", 20)
        self.multiplier = config.get("multiplier", 2.0)

    def generate_signal(self, context):
        df = context.df.copy()

        if len(df) < self.window + 1:
            return None

        df["mean"] = df["close"].rolling(self.window).mean()
        df["std"] = df["close"].rolling(self.window).std()
        df["upper"] = df["mean"] + self.multiplier * df["std"]
        df["lower"] = df["mean"] - self.multiplier * df["std"]

        close = df["close"].iloc[-1]
        upper = df["upper"].iloc[-1]
        lower = df["lower"].iloc[-1]

        if pd.isna(upper) or pd.isna(lower):
            return None

        if close > upper:
            return Signal("buy", context.symbol, context.time, close=round(close, 4), upper=round(upper, 4))
        elif close < lower:
            return Signal("sell", context.symbol, context.time, close=round(close, 4), lower=round(lower, 4))
        return None
