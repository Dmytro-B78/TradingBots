# ============================================
# File: C:\TradingBots\NT\bot_ai\strategy\sma_reversal.py
# Purpose: SMA reversal strategy class definition (fixed: added self to method)
# Encoding: UTF-8 without BOM
# ============================================

import pandas as pd
from bot_ai.strategy.base_strategy import BaseStrategy

class SmaReversalStrategy(BaseStrategy):
    def generate_signal(self, df: pd.DataFrame, params: dict):
        sma_period = params.get("sma_period", 20)
        threshold = params.get("threshold", 0.01)

        df["sma"] = df["close"].rolling(sma_period).mean()
        deviation = (df["close"] - df["sma"]) / df["sma"]

        if deviation.iloc[-1] < -threshold:
            return self.create_signal("buy", df)
        elif deviation.iloc[-1] > threshold:
            return self.create_signal("sell", df)
        return None
