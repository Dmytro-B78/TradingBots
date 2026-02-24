# ============================================
# File: C:\TradingBots\NT\bot_ai\strategy\rsi_reversal.py
# Purpose: RSI reversal strategy class definition (fixed: inherit BaseStrategy)
# Encoding: UTF-8 without BOM
# ============================================

import pandas as pd
from bot_ai.strategy.base_strategy import BaseStrategy

class RsiReversalStrategy(BaseStrategy):
    def generate_signal(self, df: pd.DataFrame, params: dict):
        rsi_period = params.get("rsi_period", 14)
        lower_threshold = params.get("lower_threshold", 30)
        upper_threshold = params.get("upper_threshold", 70)

        delta = df["close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(rsi_period).mean()
        avg_loss = loss.rolling(rsi_period).mean()
        rs = avg_gain / avg_loss
        df["rsi"] = 100 - (100 / (1 + rs))

        rsi = df["rsi"].iloc[-1]

        if rsi < lower_threshold:
            return self.create_signal("buy", df)
        elif rsi > upper_threshold:
            return self.create_signal("sell", df)
        return None
