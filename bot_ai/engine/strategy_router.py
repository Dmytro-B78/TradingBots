# ================================================================
# File: bot_ai/engine/strategy_router.py
# NT-Tech StrategyRouter 3.0 (ConfigLoader 3.0 compatible)
# ASCII-only
# ================================================================

from bot_ai.engine.file_logger import FileLogger
from bot_ai.strategy.meta_strategy import MetaStrategy

from bot_ai.strategy.ma_crossover_strategy import MACrossoverStrategy
from bot_ai.strategy.rsi_strategy import RSIStrategy
from bot_ai.strategy.macd_strategy import MACDStrategy
from bot_ai.strategy.bollinger_strategy import BollingerStrategy


class StrategyRouter:
    """
    NT-Tech Strategy Router 3.0
    Supports:
        - MetaStrategy (primary)
        - Strategy blocks inside config["strategies"]
    """

    def __init__(self, config):
        self.config = config

        # registry of supported strategies
        self.registry = {
            "ma_crossover": MACrossoverStrategy,
            "rsi": RSIStrategy,
            "macd": MACDStrategy,
            "bollinger": BollingerStrategy
        }

    # ------------------------------------------------------------
    # Select and run strategy
    # ------------------------------------------------------------
    def run(self, candles):

        # --------------------------------------------------------
        # MetaStrategy is always primary
        # --------------------------------------------------------
        meta_cfg = self.config.get("meta_strategy", None)
        if not isinstance(meta_cfg, dict):
            raise Exception("Config missing required block: meta_strategy")

        FileLogger.info("Selected strategy: meta_strategy")

        strategy = MetaStrategy(self.config)
        return strategy.run(candles)
