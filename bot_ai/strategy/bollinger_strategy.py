# ================================================================
# File: bot_ai/strategy/bollinger_strategy.py
# NT-Tech Bollinger Strategy 3.1 (no ATR filter)
# ASCII-only
# ================================================================

import math


class BollingerStrategy:
    """
    NT-Tech Bollinger Strategy 3.1
    - incremental SMA + variance
    - no ATR filter (handled by MetaStrategy)
    - no trend filter (handled by MetaStrategy)
    - O(1) per candle
    """

    def __init__(self, params=None):
        self.params = params if isinstance(params, dict) else {}

        self.period = self.params.get("period", 20)
        self.mult = self.params.get("mult", 2.0)

        self.cooldown_bars = self.params.get("cooldown", 3)
        self.cooldown_counter = 0

        self.position = "FLAT"
        self.closes = []

        self.mean = 0.0
        self.M2 = 0.0
        self.count = 0

        self.prev_price = None
        self.prev_lower = None
        self.prev_upper = None

    # ------------------------------------------------------------
    # Incremental Bollinger Bands
    # ------------------------------------------------------------
    def update_bands(self, price):
        self.count += 1

        if self.count == 1:
            self.mean = price
            self.M2 = 0.0
            return None, None, None

        delta = price - self.mean
        self.mean += delta / self.count
        delta2 = price - self.mean
        self.M2 += delta * delta2

        if self.count < self.period:
            return None, None, None

        variance = self.M2 / (self.count - 1)
        std = math.sqrt(variance)

        upper = self.mean + self.mult * std
        lower = self.mean - self.mult * std

        return lower, self.mean, upper

    # ------------------------------------------------------------
    # Main signal
    # ------------------------------------------------------------
    def on_candle(self, candle):
        price = candle.get("close")
        if price is None:
            return None

        self.closes.append(price)

        if self.cooldown_counter > 0:
            self.cooldown_counter -= 1
            return None

        lower, mid, upper = self.update_bands(price)
        if lower is None:
            return None

        if self.prev_price is None:
            self.prev_price = price
            self.prev_lower = lower
            self.prev_upper = upper
            return None

        buy_reentry = self.prev_price < self.prev_lower and price >= lower
        sell_reentry = self.prev_price > self.prev_upper and price <= upper

        self.prev_price = price
        self.prev_lower = lower
        self.prev_upper = upper

        if buy_reentry and self.position != "LONG":
            self.position = "LONG"
            self.cooldown_counter = self.cooldown_bars
            return "BUY"

        if sell_reentry and self.position != "SHORT":
            self.position = "SHORT"
            self.cooldown_counter = self.cooldown_bars
            return "SELL"

        return None
