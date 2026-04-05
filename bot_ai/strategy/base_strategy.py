# ================================================================
# File: bot_ai/strategy/base_strategy.py
# Module: strategy.base_strategy
# Purpose: NT-Tech base class for all strategies
# Responsibilities:
#   - Maintain price buffer
#   - Provide update() and on_candle() hooks
#   - Define unified NT-Tech strategy interface
# Notes:
#   - ASCII-only
# ================================================================

class BaseStrategy:
    """
    NT-Tech base class for all trading strategies.
    Provides:
        - params dict
        - price buffer
        - update(price)
        - signal() -> dict or None
        - on_candle(candle)
    """

    def __init__(self, params=None):
        self.params = params or {}
        self.prices = []

    def update(self, price):
        self.prices.append(price)

    def signal(self):
        return None

    def on_candle(self, candle):
        price = candle["close"]
        self.update(price)
        return self.signal()
