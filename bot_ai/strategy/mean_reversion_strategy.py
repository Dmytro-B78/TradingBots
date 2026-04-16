# ================================================================
# File: bot_ai/strategy/mean_reversion_strategy.py
# NT-Tech Mean Reversion Strategy (MetaStrategy-compatible)
# ASCII-only, deterministic
# ================================================================

from bot_ai.strategy.base_strategy import BaseStrategy
import math


class MeanReversionStrategy(BaseStrategy):
    """
    NT-Tech mean reversion strategy.
    BUY when price deviates far below mean.
    SELL when price deviates far above mean.
    """

    def __init__(self, params=None):
        super().__init__(params)
        self.period = int(self.params.get("period", 20))
        self.threshold = float(self.params.get("threshold", 2.0))
        self.prices = []
        self.regime = None

    # ------------------------------------------------------------
    # Optional regime hook (used by MetaStrategy if available)
    # ------------------------------------------------------------
    def set_regime(self, regime):
        self.regime = regime

    # ------------------------------------------------------------
    # Simple moving average
    # ------------------------------------------------------------
    def sma(self, values):
        if len(values) < self.period:
            return None
        return sum(values[-self.period:]) / float(self.period)

    # ------------------------------------------------------------
    # Standard deviation
    # ------------------------------------------------------------
    def std(self, values):
        if len(values) < self.period:
            return None
        mean = self.sma(values)
        if mean is None:
            return None
        var = sum((v - mean) ** 2 for v in values[-self.period:]) / float(self.period)
        return math.sqrt(var)

    # ------------------------------------------------------------
    # Main candle handler (MetaStrategy-compatible)
    # Expects candle: dict with at least "close" key
    # Returns: "BUY", "SELL" or None
    # ------------------------------------------------------------
    def on_candle(self, candle):
        price = candle["close"]
        self.prices.append(price)

        if len(self.prices) < self.period:
            return None

        mean = self.sma(self.prices)
        sd = self.std(self.prices)

        if mean is None or sd is None or sd == 0.0:
            return None

        z = (price - mean) / sd

        if z <= -self.threshold:
            return "BUY"

        if z >= self.threshold:
            return "SELL"

        return None
