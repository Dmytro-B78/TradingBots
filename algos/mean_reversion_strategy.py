# ================================================================
# File: algos/mean_reversion_strategy.py
# NT-Tech Algo: Mean Reversion (lightweight version)
# ASCII-only
# ================================================================

class MeanReversionAlgo:
    """
    Lightweight mean reversion algo.
    Designed for fast execution inside StrategyRouter.
    """

    def __init__(self, params=None):
        self.params = params or {}
        self.period = int(self.params.get("period", 20))
        self.threshold = float(self.params.get("threshold", 2.0))
        self.buffer = []

    def update(self, price):
        self.buffer.append(price)

    def sma(self):
        if len(self.buffer) < self.period:
            return None
        return sum(self.buffer[-self.period:]) / self.period

    def std(self):
        if len(self.buffer) < self.period:
            return None
        mean = self.sma()
        var = sum((p - mean) ** 2 for p in self.buffer[-self.period:]) / self.period
        return var ** 0.5

    def run(self, candles):
        signals = []

        for c in candles:
            price = c["close"]
            self.update(price)

            if len(self.buffer) < self.period:
                continue

            mean = self.sma()
            sd = self.std()
            if sd is None or sd == 0:
                continue

            z = (price - mean) / sd

            if z <= -self.threshold:
                signals.append({"signal": "BUY", "price": price})
            elif z >= self.threshold:
                signals.append({"signal": "SELL", "price": price})

        return {
            "signals": signals,
            "params": self.params
        }
