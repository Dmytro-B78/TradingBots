# ================================================================
# File: bot_ai/engine/strategy_engine.py
# NT-Tech strategy engine wrapper for StrategyAdvanced
# ASCII-only
# ================================================================

from bot_ai.strategy.strategy_advanced import StrategyAdvanced
from bot_ai.engine.file_logger import FileLogger


class StrategyEngine:
    """
    NT-Tech strategy engine wrapper.
    Responsible for:
        - initializing StrategyAdvanced
        - passing parameters and risk manager
        - capturing results and errors
    """

    def __init__(self, params, initial_balance, risk_manager):
        try:
            self.params = params if isinstance(params, dict) else {}
        except Exception:
            self.params = {}

        try:
            self.initial_balance = float(initial_balance)
        except Exception:
            self.initial_balance = 0.0

        self.risk_manager = risk_manager

    # ------------------------------------------------------------
    # Run strategy
    # ------------------------------------------------------------
    def run(self, candles):
        try:
            FileLogger.info("StrategyEngine starting StrategyAdvanced")

            strategy = StrategyAdvanced(
                params=self.params,
                initial_balance=self.initial_balance,
                risk_manager=self.risk_manager
            )

            result = strategy.run(candles)

            if not isinstance(result, dict):
                raise Exception("Strategy returned invalid result format")

            return {
                "initial_balance": result.get("initial_balance", self.initial_balance),
                "final_value": result.get("final_value", self.initial_balance),
                "params": result.get("params", self.params),
                "trades": result.get("trades", []),
                "debug": result.get("debug", [])
            }

        except Exception as e:
            FileLogger.error("StrategyEngine error: " + str(e))
            return {
                "initial_balance": self.initial_balance,
                "final_value": self.initial_balance,
                "params": self.params,
                "trades": [],
                "debug": [{"error": str(e)}]
            }
