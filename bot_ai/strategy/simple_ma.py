# ============================================
# bot_ai/strategy/simple_ma.py
# Простая стратегия на основе пересечения цены и скользящей средней
# Покупка при пробое MA вверх, продажа при пробое вниз
# Совместима с BaseStrategy, MarketContext, Signal
# ============================================

import pandas as pd
from bot_ai.strategy.base_strategy import BaseStrategy
from bot_ai.core.signal import Signal

class SimpleMAStrategy(BaseStrategy):
    def __init__(self, config):
        self.period = config.get("ma_period", 20)

    def generate_signal(self, context):
        df = context.df.copy()

        if len(df) < self.period + 2:
            return None

        df["ma"] = df["close"].rolling(self.period).mean()

        prev_close = df["close"].iloc[-2]
        curr_close = df["close"].iloc[-1]
        prev_ma = df["ma"].iloc[-2]
        curr_ma = df["ma"].iloc[-1]

        if pd.isna(prev_ma) or pd.isna(curr_ma):
            return None

        # Пересечение снизу вверх → покупка
        if prev_close < prev_ma and curr_close > curr_ma:
            return Signal("buy", context.symbol, context.time, ma=curr_ma)

        # Пересечение сверху вниз → продажа
        if prev_close > prev_ma and curr_close < curr_ma:
            return Signal("sell", context.symbol, context.time, ma=curr_ma)

        return None

