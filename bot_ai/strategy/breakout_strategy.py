# ================================================================
# File: bot_ai/strategy/breakout_strategy.py
# NT-Tech Breakout Strategy
# ASCII-only
# ================================================================

from bot_ai.strategy.base_strategy import BaseStrategy


class BreakoutStrategy(BaseStrategy):
    """
    NT-Tech breakout strategy.
    BUY when price breaks above resistance.
    SELL when price breaks below support.
    """

    def __init__(self, params=None):
        super().__init__(params)
        self.lookback = int(self.params.get("lookback", 20))

    # ------------------------------------------------------------
    # Breakout signal
    # ------------------------------------------------------------
    def signal(self):
        if len(self.prices) < self.lookback + 1:
            return None

        recent = self.prices[-self.lookback:]
        price = self.prices[-1]

        resistance = max(recent)
        support = min(recent)

        if price > resistance:
            return "BUY"

        if price < support:
            return "SELL"

        return None
