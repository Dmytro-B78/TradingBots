# ============================================
# File: C:\TradingBots\NT\bot_ai\strategy\breakout.py
# Purpose: Breakout strategy class definition (fixed: added params argument)
# Encoding: UTF-8 without BOM
# ============================================

import pandas as pd
from bot_ai.strategy.base_strategy import BaseStrategy

class BreakoutStrategy(BaseStrategy):
    def generate_signal(self, df: pd.DataFrame, params: dict):
        window = params.get("window", 20)

        df["high_max"] = df["high"].rolling(window=window).max()
        df["low_min"] = df["low"].rolling(window=window).min()

        if df["close"].iloc[-1] > df["high_max"].iloc[-2]:
            return self.create_signal("buy", df)
        elif df["close"].iloc[-1] < df["low_min"].iloc[-2]:
            return self.create_signal("sell", df)
        return None
