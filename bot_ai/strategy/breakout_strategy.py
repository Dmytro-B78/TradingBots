# ================================================================
# File: bot_ai/strategy/breakout_strategy.py
# NT-Tech Breakout Strategy (MetaStrategy-compatible)
# Fixed: exclude current candle from breakout window
# ASCII-only, deterministic
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
        self.prices = []
        self.regime = None

    # ------------------------------------------------------------
    # Optional regime hook
    # ------------------------------------------------------------
    def set_regime(self, regime):
        self.regime = regime

    # ------------------------------------------------------------
    # Main candle handler (MetaStrategy-compatible)
    # Expects candle: dict with at least "close" key
    # Returns: "BUY", "SELL" or None
    # ------------------------------------------------------------
    def on_candle(self, candle):
        price = candle["close"]
        self.prices.append(price)

        if len(self.prices) < self.lookback + 1:
            return None

        # Use previous window only (exclude current candle)
        recent = self.prices[-(self.lookback + 1):-1]

        resistance = max(recent)
        support = min(recent)

        if price > resistance:
            return "BUY"

        if price < support:
            return "SELL"

        return None
