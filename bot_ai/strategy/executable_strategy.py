# -*- coding: utf-8 -*-
# ============================================
# 📂 File: bot_ai/strategy/executable_strategy.py
# 🧪 Назначение: Реализация исполнения сигналов и логики сделок
# ============================================

import logging
from bot_ai.strategy.base_strategy import BaseStrategy
from bot_ai.execution.mock_executor import MockExecutor


class ExecutableStrategy(BaseStrategy):
    def __init__(self, cfg, pair, timeframe):
        super().__init__(cfg, pair, timeframe)
        self.executor = MockExecutor()
        self.trades = []
        self.log = logging.getLogger(self.__class__.__name__)

    def run_backtest(self) -> dict:
        if self.data.empty:
            raise ValueError("Нет данных для бэктеста")
        if self.signals.empty:
            self.log.warning("[STRATEGY] Нет сигналов, бэктест будет пустым")

        for i, signal in enumerate(self.signals):
            price = float(self.data["close"].iloc[i])
            self.executor.execute(signal, price, i)

        self.trades = self.executor.trades

        return {
            "pair": self.pair,
            "timeframe": self.timeframe,
            "signal": int(self.signals.iloc[-1]) if not self.signals.empty else 0
        }

    def summary(self):
        total = len(self.trades)
        wins = sum(1 for t in self.trades if t["pnl"] > 0)
        losses = total - wins
        avg_pnl = sum(t["pnl"] for t in self.trades) / total if total else 0.0
        return {
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "avg_pnl": round(avg_pnl, 6)
        }
