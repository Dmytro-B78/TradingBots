# -*- coding: utf-8 -*-
# 📂 File: bot_ai/strategy/rsi_bbands.py
# 📊 Назначение: RSI + Bollinger Bands
# ============================================

import pandas as pd
from bot_ai.strategy.executable_strategy import ExecutableStrategy


class RSIBBandsStrategy(ExecutableStrategy):
    def load_data(self, df: pd.DataFrame):
        self.data = df.copy()
        self.data["rsi"] = self.data["close"].rolling(self.cfg["rsi_period"]).apply(
            lambda x: 100 - (100 / (1 + (x.diff().clip(lower=0).sum() / abs(x.diff().clip(upper=0)).sum())))
        )
        self.data["ma"] = self.data["close"].rolling(self.cfg["bb_period"]).mean()
        self.data["std"] = self.data["close"].rolling(self.cfg["bb_period"]).std()
        self.data["upper"] = self.data["ma"] + self.cfg["bb_mult"] * self.data["std"]
        self.data["lower"] = self.data["ma"] - self.cfg["bb_mult"] * self.data["std"]

    def generate_signals(self):
        signals = []
        for i in range(len(self.data)):
            rsi = self.data["rsi"].iloc[i]
            price = self.data["close"].iloc[i]
            upper = self.data["upper"].iloc[i]
            lower = self.data["lower"].iloc[i]

            if pd.isna(rsi) or pd.isna(upper) or pd.isna(lower):
                signals.append(0)
                continue

            if rsi < self.cfg["rsi_oversold"] and price < lower:
                signals.append(1)
            elif rsi > self.cfg["rsi_overbought"] and price > upper:
                signals.append(-1)
            else:
                signals.append(0)
        self.signals = pd.Series(signals)
