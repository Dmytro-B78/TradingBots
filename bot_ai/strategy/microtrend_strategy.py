# ================================================================
# NT-Tech MicroTrend Strategy 2.0
# Stability mode for SOLUSDT 5m
# ASCII-only, deterministic, no Cyrillic
# ================================================================

class MicroTrendStrategy:
    def __init__(self, config=None):
        self.period = 8
        self.prices = []
        self.min_history = self.period + 2

        # stability filters
        self.min_move = 0.003   # 0.3% move required
        self.cooldown = 0
        self.cooldown_period = 3

    def on_candle(self, c):
        price = c["close"]
        self.prices.append(price)

        if self.cooldown > 0:
            self.cooldown -= 1
            return None

        if len(self.prices) < self.min_history:
            return None

        window = self.prices[-self.period:]
        start = window[0]
        end = window[-1]

        if start == 0:
            return None

        change = (end - start) / start

        # weak-signal filter
        if abs(change) < self.min_move:
            return None

        # BUY
        if change > 0:
            self.cooldown = self.cooldown_period
            return "BUY"

        # SELL
        if change < 0:
            self.cooldown = self.cooldown_period
            return "SELL"

        return None
