# -*- coding: utf-8 -*-
# ============================================
# 📂 File: bot_ai/strategy/rsi_macd.py
# 📈 Назначение: RSI + MACD стратегия
# ============================================

import pandas as pd
from bot_ai.strategy.executable_strategy import ExecutableStrategy


class RSIMACDStrategy(ExecutableStrategy):
    def load_data(self, df: pd.DataFrame):
        self.data = df.copy()
        self.data["rsi"] = self.data["close"].rolling(self.cfg["rsi_period"]).apply(
            lambda x: 100 - (100 / (1 + (x.diff().clip(lower=0).sum() / abs(x.diff().clip(upper=0)).sum())))
        )
        self.data["ema_fast"] = self.data["close"].ewm(span=self.cfg["macd_fast"], adjust=False).mean()
        self.data["ema_slow"] = self.data["close"].ewm(span=self.cfg["macd_slow"], adjust=False).mean()
        self.data["macd"] = self.data["ema_fast"] - self.data["ema_slow"]
        self.data["macd_signal"] = self.data["macd"].ewm(span=self.cfg["macd_signal"], adjust=False).mean()

    def generate_signals(self):
        signals = []
        for i in range(len(self.data)):
            rsi = self.data["rsi"].iloc[i]
            macd = self.data["macd"].iloc[i]
            signal = self.data["macd_signal"].iloc[i]

            if pd.isna(rsi) or pd.isna(macd) or pd.isna(signal):
                signals.append(0)
                continue

            if rsi < self.cfg["rsi_oversold"] and macd > signal:
                signals.append(1)   # BUY
            elif rsi > self.cfg["rsi_overbought"] and macd < signal:
                signals.append(-1)  # SELL
            else:
                signals.append(0)   # HOLD

        self.signals = pd.Series(signals)
