# ================================================================
# File: bot_ai/engine/optimizer.py
# NT-Tech Optimizer 1.0 (ASCII-only)
# Deterministic parameter optimizer for MetaStrategy 3.0
# ================================================================

import itertools
from bot_ai.engine.trade_analyzer import TradeAnalyzer
from bot_ai.engine.backtest_engine import BacktestEngine


class Optimizer:
    """
    NT-Tech Optimizer 1.0
    - ASCII-only
    - deterministic grid search
    - evaluates parameter combinations using:
        * BacktestEngine
        * TradeAnalyzer 3.1
    """

    def __init__(self, param_grid, candles):
        """
        param_grid: dict of lists
            {
                "ma.fast": [5, 10, 20],
                "ma.slow": [50, 100],
                "macd.fast": [8, 12],
                "macd.slow": [20, 26],
                "macd.signal": [9],
                ...
            }

        candles: list of OHLCV candles
        """
        self.param_grid = param_grid
        self.candles = candles

    # ------------------------------------------------------------
    # Build parameter combinations
    # ------------------------------------------------------------
    def build_combinations(self):
        keys = list(self.param_grid.keys())
        values = [self.param_grid[k] for k in keys]

        for combo in itertools.product(*values):
            params = {}
            for i, key in enumerate(keys):
                params[key] = combo[i]
            yield params

    # ------------------------------------------------------------
    # Convert flat params to nested dict for MetaStrategy
    # ------------------------------------------------------------
    def nest_params(self, flat):
        nested = {
            "ma": {},
            "macd": {},
            "rsi": {},
            "boll": {},
        }

        for k, v in flat.items():
            if k.startswith("ma."):
                nested["ma"][k.split(".")[1]] = v
            elif k.startswith("macd."):
                nested["macd"][k.split(".")[1]] = v
            elif k.startswith("rsi."):
                nested["rsi"][k.split(".")[1]] = v
            elif k.startswith("boll."):
                nested["boll"][k.split(".")[1]] = v

        return nested

    # ------------------------------------------------------------
    # Evaluate a single parameter set
    # ------------------------------------------------------------
    def evaluate(self, params):
        nested = self.nest_params(params)

        engine = BacktestEngine(
            candles=self.candles,
            strategy_params=nested
        )

        engine.run()

        analyzer = TradeAnalyzer()
        metrics = analyzer.run()

        return metrics

    # ------------------------------------------------------------
    # Run optimization
    # ------------------------------------------------------------
    def run(self):
        best_params = None
        best_score = -999999.0
        best_metrics = None

        for params in self.build_combinations():
            metrics = self.evaluate(params)

            if metrics is None:
                continue

            score = (
                metrics["profit_factor"] * 2.0 +
                metrics["expectancy"] * 1.0 -
                metrics["max_drawdown"] * 0.1
            )

            if score > best_score:
                best_score = score
                best_params = params
                best_metrics = metrics

        return {
            "best_params": best_params,
            "best_metrics": best_metrics,
            "best_score": best_score,
        }
