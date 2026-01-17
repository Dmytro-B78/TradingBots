# -*- coding: utf-8 -*-
# 📂 File: bot_ai/strategy/range.py
# 📊 Назначение: Range стратегия
# ============================================

import pandas as pd
from bot_ai.strategy.executable_strategy import ExecutableStrategy


class RangeStrategy(ExecutableStrategy):
    def load_data(self, df: pd.DataFrame):
        self.data = df.copy()
        self.data["mid"] = (self.data["high"] + self.data["low"]) / 2

    def generate_signals(self):
        signals = []
        for i in range(len(self.data)):
            price = self.data["close"].iloc[i]
            mid = self.data["mid"].iloc[i]
            if price < mid * 0.98:
                signals.append(1)
            elif price > mid * 1.02:
                signals.append(-1)
            else:
                signals.append(0)
        self.signals = pd.Series(signals)
