# ============================================
# bot_ai/strategy/sl_tp.py
# Стратегия на основе фиксированных SL/TP процентов
# Покупка при падении цены на SL%, продажа при росте на TP%
# Совместима с BaseStrategy, MarketContext, Signal
# ============================================

import pandas as pd
from bot_ai.strategy.base_strategy import BaseStrategy
from bot_ai.core.signal import Signal

class SlTpStrategy(BaseStrategy):
    def __init__(self, config):
        self.sl_pct = config.get("sl_pct", 0.01)   # 1% падение → покупка
        self.tp_pct = config.get("tp_pct", 0.02)   # 2% рост → продажа

    def generate_signal(self, context):
        df = context.df.copy()

        if len(df) < 2:
            return None

        prev_close = df["close"].iloc[-2]
        curr_close = df["close"].iloc[-1]
        change = (curr_close - prev_close) / prev_close

        if change > self.tp_pct:
            return Signal("sell", context.symbol, context.time, change=round(change, 4))
        elif change < -self.sl_pct:
            return Signal("buy", context.symbol, context.time, change=round(change, 4))
        else:
            return None

