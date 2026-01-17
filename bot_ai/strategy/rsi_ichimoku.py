# -*- coding: utf-8 -*-
# 📂 File: bot_ai/strategy/rsi_ichimoku.py
# 📊 Назначение: RSI + Ichimoku стратегия
# ============================================

import pandas as pd
from bot_ai.strategy.executable_strategy import ExecutableStrategy


class RSIIchimokuStrategy(ExecutableStrategy):
    def load_data(self, df: pd.DataFrame):
        self.data = df.copy()
        high = self.data["high"]
        low = self.data["low"]
        close = self.data["close"]

        self.data["tenkan"] = (high.rolling(9).max() + low.rolling(9).min()) / 2
        self.data["kijun"] = (high.rolling(26).max() + low.rolling(26).min()) / 2
        self.data["rsi"] = close.rolling(self.cfg["rsi_period"]).apply(
            lambda x: 100 - (100 / (1 + (x.diff().clip(lower=0).sum() / abs(x.diff().clip(upper=0)).sum())))
        )

    def generate_signals(self):
        signals = []
        for i in range(len(self.data)):
            rsi = self.data["rsi"].iloc[i]
            tenkan = self.data["tenkan"].iloc[i]
            kijun = self.data["kijun"].iloc[i]
            price = self.data["close"].iloc[i]

            if pd.isna(rsi) or pd.isna(tenkan) or pd.isna(kijun):
                signals.append(0)
                continue

            if rsi < self.cfg["rsi_oversold"] and price > tenkan > kijun:
                signals.append(1)
            elif rsi > self.cfg["rsi_overbought"] and price < tenkan < kijun:
                signals.append(-1)
            else:
                signals.append(0)
        self.signals = pd.Series(signals)
