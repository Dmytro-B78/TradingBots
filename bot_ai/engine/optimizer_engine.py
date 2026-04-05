# ================================================================
# File: bot_ai/engine/optimizer_engine.py
# Module: engine.optimizer_engine
# Purpose: NT-Tech strategy parameter optimizer
# Responsibilities:
#   - Run parameter sweeps
#   - Execute backtests for each parameter set
#   - Track performance metrics
#   - Select best-performing configuration
# Notes:
#   - ASCII-only
# ================================================================

import itertools
from bot_ai.engine.backtest_engine import BacktestEngine


class OptimizerEngine:
    """
    NT-Tech strategy optimizer.
    """

    def __init__(self, strategy_class, param_grid, candles):
        self.strategy_class = strategy_class
        self.param_grid = param_grid
        self.candles = candles
        self.results = []

    def generate_param_sets(self):
        keys = list(self.param_grid.keys())
        values = list(self.param_grid.values())
        for combo in itertools.product(*values):
            yield dict(zip(keys, combo))

    def run(self):
        for params in self.generate_param_sets():
            engine = BacktestEngine(self.strategy_class, params, self.candles)
            result = engine.run()

            self.results.append({
                "params": params,
                "result": result
            })

        return self.results

    def best(self, metric="net_profit"):
        if not self.results:
            return None

        sorted_results = sorted(
            self.results,
            key=lambda r: r["result"].get(metric, 0),
            reverse=True
        )
        return sorted_results[0]
