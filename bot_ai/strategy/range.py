# ============================================
# File: C:\TradingBots\NT\bot_ai\strategy\range.py
# Purpose: Range strategy class definition (fixed: added params argument)
# Encoding: UTF-8 without BOM
# ============================================

import pandas as pd
from bot_ai.strategy.base_strategy import BaseStrategy

class RangeStrategy(BaseStrategy):
    def generate_signal(self, df: pd.DataFrame, params: dict):
        window = params.get("window", 20)
        buffer = params.get("buffer", 0.01)

        df["high_max"] = df["high"].rolling(window=window).max()
        df["low_min"] = df["low"].rolling(window=window).min()

        upper = df["high_max"].iloc[-1] * (1 - buffer)
        lower = df["low_min"].iloc[-1] * (1 + buffer)
        price = df["close"].iloc[-1]

        if price < lower:
            return self.create_signal("buy", df)
        elif price > upper:
            return self.create_signal("sell", df)
        return None
