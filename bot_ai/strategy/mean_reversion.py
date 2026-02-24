# ============================================
# File: C:\TradingBots\NT\bot_ai\strategy\mean_reversion.py
# Purpose: Mean reversion strategy class definition (fixed: added params argument)
# Encoding: UTF-8 without BOM
# ============================================

import pandas as pd
from bot_ai.strategy.base_strategy import BaseStrategy

class MeanReversionStrategy(BaseStrategy):
    def generate_signal(self, df: pd.DataFrame, params: dict):
        window = params.get("window", 20)
        threshold = params.get("threshold", 0.02)

        df["sma"] = df["close"].rolling(window=window).mean()
        deviation = (df["close"] - df["sma"]) / df["sma"]

        if deviation.iloc[-1] < -threshold:
            return self.create_signal("buy", df)
        elif deviation.iloc[-1] > threshold:
            return self.create_signal("sell", df)
        return None
