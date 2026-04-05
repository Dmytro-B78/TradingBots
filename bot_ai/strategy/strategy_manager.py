# ================================================================
# File: bot_ai/strategy/strategy_manager.py
# Module: strategy.strategy_manager
# Purpose: NT-Tech strategy loader and registry
# Responsibilities:
#   - Register available strategies
#   - Instantiate strategy classes dynamically
#   - Validate parameter sets
# Notes:
#   - ASCII-only
# ================================================================

from bot_ai.strategy.ma_crossover_strategy import MACrossoverStrategy
from bot_ai.strategy.bollinger_strategy import BollingerStrategy
from bot_ai.strategy.macd_strategy import MACDStrategy
from bot_ai.strategy.rsi_strategy import RSIStrategy
from bot_ai.strategy.meta_strategy import MetaStrategy


class StrategyManager:
    """
    NT-Tech strategy registry and loader.
    """

    REGISTRY = {
        "ma_crossover": MACrossoverStrategy,
        "bollinger": BollingerStrategy,
        "macd": MACDStrategy,
        "rsi": RSIStrategy,
        "meta": MetaStrategy
    }

    @classmethod
    def list(cls):
        return list(cls.REGISTRY.keys())

    @classmethod
    def load(cls, name, params=None):
        if name not in cls.REGISTRY:
            raise ValueError(f"Unknown strategy: {name}")

        strategy_class = cls.REGISTRY[name]
        params = params or {}

        return strategy_class(**params)
