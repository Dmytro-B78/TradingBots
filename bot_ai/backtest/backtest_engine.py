# ================================================================
# File: bot_ai/backtest/backtest_engine.py
# Module: backtest.backtest_engine
# Purpose: NT-Tech Backtest Engine
# Responsibilities:
#   - Load historical data
#   - Feed candles into strategy
#   - Process signals through logic pipeline
#   - Simulate order execution
#   - Track PnL, trades, winrate
# Notes:
#   - ASCII-only
# ================================================================

import pandas as pd

from bot_ai.strategy.strategy_manager import StrategyManager
from bot_ai.logic.signal_pipeline import SignalPipeline
from bot_ai.logic.risk_engine import RiskEngine


class BacktestEngine:
    """
    NT-Tech Backtest Engine.
    """

    def __init__(self, strategy_name, symbol):
        self.symbol = symbol.upper()

        # Strategy
        self.strategy_manager = StrategyManager()
        self.strategy = self.strategy_manager.load(strategy_name)

        # Logic
        self.pipeline = SignalPipeline()
        self.risk = RiskEngine()

        # Results
        self.trades = []
        self.position = 0
        self.entry_price = None
        self.pnl = 0.0

    # ------------------------------------------------------------
    # Execution simulator
    # ------------------------------------------------------------
    def _execute(self, decision, price):
        side = decision.get("side")
        size = decision.get("size", 1)

        if side == "BUY" and self.position == 0:
            self.position = size
            self.entry_price = price

        elif side == "SELL" and self.position > 0:
            profit = (price - self.entry_price) * self.position
            self.pnl += profit
            self.trades.append(profit)
            self.position = 0
            self.entry_price = None

    # ------------------------------------------------------------
    # Backtest runner
    # ------------------------------------------------------------
    def run(self, df):
        for _, candle in df.iterrows():
            price = candle["close"]
            signal = self.strategy.on_candle(candle)

            if signal is None:
                continue

            pipeline_output = self.pipeline.process(signal, price)
            decision = self.risk.decide(pipeline_output, price)

            if decision:
                self._execute(decision, price)

        winrate = (
            sum(1 for t in self.trades if t > 0) / len(self.trades) * 100
            if self.trades else 0
        )

        return {
            "pnl": self.pnl,
            "trades": self.trades,
            "winrate": winrate
        }
