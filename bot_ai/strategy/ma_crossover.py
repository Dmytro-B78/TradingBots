# ============================================
# File: C:\TradingBots\NT\bot_ai\strategy\ma_crossover.py
# Purpose: MA crossover strategy class definition (fixed: added self to method)
# Encoding: UTF-8 without BOM
# ============================================

import pandas as pd
from bot_ai.strategy.base_strategy import BaseStrategy

class MaCrossoverStrategy(BaseStrategy):
    def generate_signal(self, df: pd.DataFrame, params: dict):
        fast = params.get("fast", 10)
        slow = params.get("slow", 30)

        df["ma_fast"] = df["close"].rolling(fast).mean()
        df["ma_slow"] = df["close"].rolling(slow).mean()

        if df["ma_fast"].iloc[-2] < df["ma_slow"].iloc[-2] and df["ma_fast"].iloc[-1] > df["ma_slow"].iloc[-1]:
            return self.create_signal("buy", df)
        elif df["ma_fast"].iloc[-2] > df["ma_slow"].iloc[-2] and df["ma_fast"].iloc[-1] < df["ma_slow"].iloc[-1]:
            return self.create_signal("sell", df)
        return None
