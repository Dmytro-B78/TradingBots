# ============================================
# Path: C:\TradingBots\NT\bot_ai\strategy\executable_strategy.py
# Purpose: Base class for strategies that execute trades
# Format: UTF-8 without BOM, production-ready
# ============================================

import logging
from bot_ai.strategy.base_strategy import BaseStrategy
from bot_ai.execution.mock_executor import MockExecutor

class ExecutableStrategy(BaseStrategy):
    def __init__(self, config, pair, timeframe):
        super().__init__(config)
        self.pair = pair
        self.timeframe = timeframe
        self.executor = MockExecutor()
        self.trades = []
        self.log = logging.getLogger(self.__class__.__name__)
        self.data = None
        self.signals = []

    def load_data(self, df):
        self.data = df

    def run_backtest(self) -> dict:
        if self.data is None or self.data.empty:
            raise ValueError("No data loaded for backtest.")
        if not self.signals:
            self.log.warning("[STRATEGY] No signals to execute.")
            return {}

        for i, signal in enumerate(self.signals):
            price = float(self.data["close"].iloc[i])
            self.executor.execute(signal, price, i)

        self.trades = self.executor.trades

        return {
            "pair": self.pair,
            "timeframe": self.timeframe,
            "signal": int(self.signals[-1]["signal"]) if self.signals else 0
        }

    def summary(self):
        total = len(self.trades)
        wins = sum(1 for t in self.trades if t.get("pnl", 0) > 0)
        losses = total - wins
        avg_pnl = sum(t.get("pnl", 0) for t in self.trades) / total if total else 0.0
        return {
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "avg_pnl": round(avg_pnl, 6)
        }
