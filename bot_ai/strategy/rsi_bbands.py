# ============================================
# File: bot_ai/strategy/rsi_bbands.py
# Strategy: RSI + lower Bollinger Band
# Buy when price breaks below lower BB and RSI is low
# Compatible with BaseStrategy, MarketContext, Signal
# ============================================

import pandas as pd
from bot_ai.strategy.base_strategy import BaseStrategy
from bot_ai.core.signal import Signal

class RSIBBandsStrategy(BaseStrategy):
    def __init__(self, config):
        params = config.get("params", config)
        self.bb_period = params.get("bb_period", params.get("window", 20))
        self.bb_std = params.get("bb_std", params.get("std_dev", 2.0))
        self.rsi_period = params.get("rsi_period", 14)

    def generate_signal(self, context):
        df = context.df.copy()

        if len(df) < self.bb_period + 1:
            return None

        df["ma"] = df["close"].rolling(self.bb_period).mean()
        df["std"] = df["close"].rolling(self.bb_period).std()
        df["lower"] = df["ma"] - self.bb_std * df["std"]

        delta = df["close"].diff()
        gain = delta.where(delta > 0, 0).rolling(self.rsi_period).mean()
        loss = -delta.where(delta < 0, 0).rolling(self.rsi_period).mean()
        rs = gain / (loss + 1e-6)
        df["rsi"] = 100 - (100 / (1 + rs))

        close = df["close"].iloc[-1]
        lower = df["lower"].iloc[-1]
        rsi = df["rsi"].iloc[-1]
        ma = df["ma"].iloc[-1]

        if pd.isna(lower) or pd.isna(rsi) or pd.isna(ma):
            return None

        if close < lower and rsi < 30:
            return Signal("buy", context.symbol, context.time, close=round(close, 2), rsi=round(rsi, 2))
        elif close > ma and rsi > 70:
            return Signal("sell", context.symbol, context.time, close=round(close, 2), rsi=round(rsi, 2))
        return None
