# ================================================================
# NT-Tech MACD Strategy 3.5
# Optimized for SOLUSDT 5m
# ASCII-only, deterministic, no Cyrillic
# ================================================================

class MACDStrategy:
    def __init__(self, config=None):
        # SOL-friendly MACD periods
        self.fast = 8
        self.slow = 17
        self.signal = 5

        self.prices = []
        self.ema_fast = None
        self.ema_slow = None
        self.ema_signal = None

        self.alpha_fast = 2 / (self.fast + 1)
        self.alpha_slow = 2 / (self.slow + 1)
        self.alpha_signal = 2 / (self.signal + 1)

        self.min_history = self.slow + self.signal

    def on_candle(self, c):
        price = c["close"]
        self.prices.append(price)

        if len(self.prices) < self.min_history:
            return None

        # EMA fast
        if self.ema_fast is None:
            self.ema_fast = price
        else:
            self.ema_fast = self.alpha_fast * price + (1 - self.alpha_fast) * self.ema_fast

        # EMA slow
        if self.ema_slow is None:
            self.ema_slow = price
        else:
            self.ema_slow = self.alpha_slow * price + (1 - self.alpha_slow) * self.ema_slow

        macd = self.ema_fast - self.ema_slow

        # Signal line
        if self.ema_signal is None:
            self.ema_signal = macd
        else:
            self.ema_signal = self.alpha_signal * macd + (1 - self.alpha_signal) * self.ema_signal

        hist = macd - self.ema_signal

        # weak-signal filter
        if abs(hist) < 0.05:
            return None

        # BUY
        if hist > 0 and macd > self.ema_signal:
            return "BUY"

        # SELL
        if hist < 0 and macd < self.ema_signal:
            return "SELL"

        return None
