# -*- coding: utf-8 -*-
# ============================================
# 📂 File: bot_ai/strategy/base_strategy.py
# 🧱 Назначение: Абстрактный базовый класс стратегии
# ============================================

import abc
import pandas as pd

class BaseStrategy(abc.ABC):
    def __init__(self, cfg: dict, pair: str, timeframe: str):
        self.cfg = cfg
        self.pair = pair
        self.timeframe = timeframe
        self.data = pd.DataFrame()
        self.signals = pd.Series(dtype=int)

    @abc.abstractmethod
    def load_data(self, df: pd.DataFrame):
        pass

    @abc.abstractmethod
    def generate_signals(self):
        pass

    @abc.abstractmethod
    def run_backtest(self) -> dict:
        pass
