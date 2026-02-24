# ============================================
# File: bot_ai/strategy/rsi_ichimoku.py
# Strategy: RSI growth + Tenkan > Kijun (Ichimoku)
# Buy signal when RSI rises and Tenkan crosses above Kijun
# Compatible with BaseStrategy, MarketContext, Signal
# ============================================

import pandas as pd
from bot_ai.strategy.base_strategy import BaseStrategy
from bot_ai.core.signal import Signal

class RSIIchimokuStrategy(BaseStrategy):
    def __init__(self, config):
        self.rsi_period = config.get("rsi_period", 14)
        self.tenkan_period = config.get("tenkan_period", 9)
        self.kijun_period = config.get("kijun_period", 26)

    def generate_signal(self, context):
        df = context.df.copy()

        if len(df) < max(self.rsi_period, self.kijun_period) + 1:
            return None

        df["rsi"] = df["close"].rolling(self.rsi_period).mean()
        df["tenkan"] = (df["high"].rolling(self.tenkan_period).max() + df["low"].rolling(self.tenkan_period).min()) / 2
        df["kijun"] = (df["high"].rolling(self.kijun_period).max() + df["low"].rolling(self.kijun_period).min()) / 2

        rsi_now = df["rsi"].iloc[-1]
        rsi_prev = df["rsi"].iloc[-2]
        tenkan = df["tenkan"].iloc[-1]
        kijun = df["kijun"].iloc[-1]

        if pd.isna(rsi_now) or pd.isna(rsi_prev) or pd.isna(tenkan) or pd.isna(kijun):
            return None

        if rsi_now > rsi_prev and tenkan > kijun:
            return Signal("buy", context.symbol, context.time, rsi=rsi_now, tenkan=tenkan, kijun=kijun)
        return None
