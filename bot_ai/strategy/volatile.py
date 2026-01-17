# -*- coding: utf-8 -*-
# 📂 File: bot_ai/strategy/volatile.py
# 📊 Назначение: Волатильная стратегия
# ============================================

import pandas as pd
from bot_ai.strategy.executable_strategy import ExecutableStrategy


class VolatileStrategy(ExecutableStrategy):
    def load_data(self, df: pd.DataFrame):
        self.data = df.copy()
        self.data["range"] = self.data["high"] - self.data["low"]

    def generate_signals(self):
        signals = []
        for i in range(len(self.data)):
            r = self.data["range"].iloc[i]
            if r > self.data["range"].rolling(10).mean().iloc[i] * 1.5:
                signals.append(1)
            else:
                signals.append(0)
        self.signals = pd.Series(signals)
