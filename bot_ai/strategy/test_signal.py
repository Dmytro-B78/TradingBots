# ============================================
# File: bot_ai/strategy/test_signal.py
# Назначение: Тестовая стратегия для отладки пайплайна
# Генерирует сигналы на каждом втором баре
# ============================================

import logging
from bot_ai.strategy.executable_strategy import ExecutableStrategy
import pandas as pd

class TestSignalStrategy(ExecutableStrategy):
    def __init__(self, config, symbol, timeframe):
        super().__init__(config, symbol, timeframe)
        self.symbol = symbol  # ✅ Исправлено: сохраняем symbol
        self.signals = []

    def load_data(self, df: pd.DataFrame):
        self.df = df
        logging.debug(f"[TestSignalStrategy] Загружены данные: {len(df)} свечей")

    def generate_signal(self, i: int):
        # Абстрактный метод из ExecutableStrategy — обязателен, даже если не используется
        pass

    def generate_signals(self):
        logging.debug(f"[TestSignalStrategy] Генерация сигналов для {self.symbol}")
        for i in range(1, len(self.df), 2):
            row = self.df.iloc[i]
            signal = {
                "symbol": self.symbol,
                "time": int(row["time"]),
                "signal": "buy" if i % 4 == 1 else "sell",
                "price": row["close"],
                "entry_time": int(row["time"]),
                "pnl": 0.01 if i % 4 == 1 else -0.005
            }
            self.signals.append(signal)

    def summary(self):
        trades = len(self.signals)
        wins = sum(1 for s in self.signals if s["pnl"] > 0)
        losses = trades - wins
        avg_pnl = round(sum(s["pnl"] for s in self.signals) / trades, 4) if trades else 0.0
        return {
            "total_trades": trades,
            "wins": wins,
            "losses": losses,
            "avg_pnl": avg_pnl
        }
