# ============================================
# Path: C:\TradingBots\NT\bot_ai\strategy\countertrend.py
# Purpose: Countertrend strategy based on RSI
# Logic: Buy on oversold, sell on overbought
# Compatible with: BaseStrategy, MarketContext, Signal
# Format: UTF-8 without BOM, production-ready
# ============================================

import pandas as pd
from bot_ai.strategy.base_strategy import BaseStrategy
from bot_ai.core.signal import Signal

class CountertrendStrategy(BaseStrategy):
    def __init__(self, config):
        params = config.get("params", config)
        self.rsi_period = params.get("rsi_period", 14)
        self.lower_threshold = params.get("rsi_entry", params.get("lower_threshold", 30))
        self.upper_threshold = params.get("rsi_exit", params.get("upper_threshold", 70))

    def generate_signal(self, context):
        df = context.df.copy()

        if len(df) < self.rsi_period + 1:
            return None

        delta = df["close"].diff()
        gain = delta.where(delta > 0, 0).rolling(self.rsi_period).mean()
        loss = -delta.where(delta < 0, 0).rolling(self.rsi_period).mean()
        rs = gain / (loss + 1e-6)
        df["rsi"] = 100 - (100 / (1 + rs))

        rsi = df["rsi"].iloc[-1]

        if pd.isna(rsi):
            return None

        if rsi < self.lower_threshold:
            return Signal("buy", context.symbol, context.time, rsi=round(rsi, 2))
        elif rsi > self.upper_threshold:
            return Signal("sell", context.symbol, context.time, rsi=round(rsi, 2))
        return None
