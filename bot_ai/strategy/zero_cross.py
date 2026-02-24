# ============================================
# File: C:\TradingBots\NT\bot_ai\strategy\zero_cross.py
# Purpose: Zero-cross strategy class definition (fixed: added self to method)
# Encoding: UTF-8 without BOM
# ============================================

import pandas as pd
from bot_ai.strategy.base_strategy import BaseStrategy

class ZeroCrossStrategy(BaseStrategy):
    def generate_signal(self, df: pd.DataFrame, params: dict):
        period = params.get("period", 14)

        df["returns"] = df["close"].pct_change()
        df["signal"] = df["returns"].rolling(period).mean()

        if df["signal"].iloc[-2] < 0 and df["signal"].iloc[-1] > 0:
            return self.create_signal("buy", df)
        elif df["signal"].iloc[-2] > 0 and df["signal"].iloc[-1] < 0:
            return self.create_signal("sell", df)
        return None
