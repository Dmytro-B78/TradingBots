# ================================================================
# NT-Tech Bollinger Strategy 3.5
# Optimized for SOLUSDT 5m
# ASCII-only, deterministic, no Cyrillic
# ================================================================

class BollingerStrategy:
    def __init__(self, config=None):
        self.period = 20
        self.mult = 2.2  # SOL-friendly width
        self.prices = []
        self.min_history = self.period + 2

    def _sma(self, arr, period):
        return sum(arr[-period:]) / period

    def _std(self, arr, period):
        mean = self._sma(arr, period)
        return (sum((x - mean) ** 2 for x in arr[-period:]) / period) ** 0.5

    def on_candle(self, c):
        price = c["close"]
        self.prices.append(price)

        if len(self.prices) < self.min_history:
            return None

        sma = self._sma(self.prices, self.period)
        std = self._std(self.prices, self.period)

        upper = sma + self.mult * std
        lower = sma - self.mult * std

        # weak-signal filter
        if abs(price - sma) < std * 0.3:
            return None

        # BUY: recovery from lower band
        if price < lower:
            return "BUY"

        # SELL: rejection from upper band
        if price > upper:
            return "SELL"

        return None
