# ================================================================
# NT-Tech MA Crossover Strategy 3.6
# Stable, regime-aware, SOLUSDT 5m optimized
# ASCII-only, deterministic, no Cyrillic
# ================================================================

class MACrossoverStrategy:
    def __init__(self, config=None):
        # smoother MA for SOL 5m
        self.fast = 20
        self.slow = 50

        self.fast_ma = []
        self.slow_ma = []
        self.min_history = self.slow

        # divergence threshold (0.3%)
        self.min_divergence = 0.003

        # regime passed from MetaStrategy
        self.regime = "range"

    def set_regime(self, regime):
        self.regime = regime

    def _ma(self, arr, period):
        if len(arr) < period:
            return None
        return sum(arr[-period:]) / period

    def on_candle(self, c):
        price = c["close"]
        self.fast_ma.append(price)
        self.slow_ma.append(price)

        if len(self.slow_ma) < self.min_history:
            return None

        fast = self._ma(self.fast_ma, self.fast)
        slow = self._ma(self.slow_ma, self.slow)

        if fast is None or slow is None:
            return None

        # regime filter
        if self.regime not in ("trend", "expansion"):
            return None

        # divergence filter
        if slow == 0:
            return None

        divergence = (fast - slow) / slow

        # BUY
        if divergence > self.min_divergence:
            return "BUY"

        # SELL
        if divergence < -self.min_divergence:
            return "SELL"

        return None
