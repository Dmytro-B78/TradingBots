# ================================================================
# File: bot_ai/strategy/strategy_template.py
# Module: strategy.strategy_template
# Purpose: NT-Tech base template for new strategies
# Responsibilities:
#   - Provide a minimal extendable structure
#   - Ensure compatibility with NT-Tech strategy manager
# Notes:
#   - ASCII-only
# ================================================================

from bot_ai.strategy.base_strategy import BaseStrategy


class StrategyTemplate(BaseStrategy):
    """
    NT-Tech strategy template.
    Extend this class to build new strategies.
    """

    def __init__(self, params=None):
        super().__init__(params)
        self.params = params or {}

    def signal(self):
        return None

    def on_candle(self, candle):
        price = candle["close"]
        self.update(price)
        return self.signal()
