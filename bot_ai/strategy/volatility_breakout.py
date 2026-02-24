# ============================================
# File: C:\TradingBots\NT\bot_ai\strategy\volatility_breakout.py
# Purpose: Volatility breakout strategy class definition (fixed: added self to method)
# Encoding: UTF-8 without BOM
# ============================================

import pandas as pd
from bot_ai.strategy.base_strategy import BaseStrategy

class VolatilityBreakoutStrategy(BaseStrategy):
    def generate_signal(self, df: pd.DataFrame, params: dict):
        atr_period = params.get("atr_period", 14)
        breakout_multiplier = params.get("breakout_multiplier", 1.5)

        df["high_low"] = df["high"] - df["low"]
        df["atr"] = df["high_low"].rolling(atr_period).mean()
        breakout_level = df["close"].iloc[-2] + breakout_multiplier * df["atr"].iloc[-2]
        breakdown_level = df["close"].iloc[-2] - breakout_multiplier * df["atr"].iloc[-2]

        if df["close"].iloc[-1] > breakout_level:
            return self.create_signal("buy", df)
        elif df["close"].iloc[-1] < breakdown_level:
            return self.create_signal("sell", df)
        return None
