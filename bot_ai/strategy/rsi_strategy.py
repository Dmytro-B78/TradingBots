# ================================================================
# NT-Tech RSI Strategy 3.5
# Optimized for SOLUSDT 5m
# ASCII-only, deterministic, no Cyrillic
# ================================================================

class RSIStrategy:
    def __init__(self, config=None):
        self.period = 14
        self.gains = []
        self.losses = []
        self.prev_close = None
        self.min_history = self.period + 2

        # thresholds tuned for SOL
        self.buy_level = 35
        self.sell_level = 65

    def on_candle(self, c):
        close = c["close"]

        if self.prev_close is None:
            self.prev_close = close
            return None

        change = close - self.prev_close
        self.prev_close = close

        self.gains.append(max(change, 0))
        self.losses.append(abs(min(change, 0)))

        if len(self.gains) < self.min_history:
            return None

        avg_gain = sum(self.gains[-self.period:]) / self.period
        avg_loss = sum(self.losses[-self.period:]) / self.period

        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        # weak-signal filter
        if 45 < rsi < 55:
            return None

        # BUY: oversold recovery
        if rsi < self.buy_level:
            return "BUY"

        # SELL: overbought rejection
        if rsi > self.sell_level:
            return "SELL"

        return None
