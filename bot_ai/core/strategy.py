# ============================================
# File: C:\TradingBots\NT\bot_ai\core\strategy.py
# Purpose: Base class for strategy execution modes
# Encoding: UTF-8 without BOM
# ============================================

import pandas as pd

class Strategy:
    def __init__(self, df: pd.DataFrame, config: dict, mode: str = "backtest"):
        self.df = df.copy()
        self.config = config
        self.mode = mode
        self.df["signal"] = 0

    def generate_signals(self):
        raise NotImplementedError("generate_signals() must be implemented in subclass.")

    def get_dataframe(self):
        return self.df

    def is_live(self):
        return self.mode == "live"

    def is_backtest(self):
        return self.mode == "backtest"

    def is_paper(self):
        return self.mode == "paper"
