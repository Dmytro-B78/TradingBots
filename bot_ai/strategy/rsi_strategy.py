# ================================================================
# File: bot_ai/strategy/rsi_strategy.py
# NT-Tech RSI Strategy 3.1 (no ATR filter)
# ASCII-only
# ================================================================

class RSIStrategy:
    """
    NT-Tech RSI Strategy 3.1
    - incremental RSI (Wilder)
    - no ATR filter (handled by MetaStrategy)
    - no trend filter (handled by MetaStrategy)
    - O(1) per candle
    """

    def __init__(self, params=None):
        self.params = params if isinstance(params, dict) else {}

        self.period = self.params.get("period", 14)
        self.buy_level = self.params.get("buy", 30)
        self.sell_level = self.params.get("sell", 70)

        self.cooldown_bars = self.params.get("cooldown", 3)
        self.cooldown_counter = 0

        self.position = "FLAT"
        self.closes = []

        self.prev_price = None
        self.avg_gain = None
        self.avg_loss = None
        self.prev_rsi = None

    # ------------------------------------------------------------
    # Incremental RSI
    # ------------------------------------------------------------
    def update_rsi(self, price):
        if self.prev_price is None:
            self.prev_price = price
            return None

        change = price - self.prev_price
        gain = max(change, 0)
        loss = max(-change, 0)

        if self.avg_gain is None:
            self.avg_gain = gain
            self.avg_loss = loss
            self.prev_price = price
            return None

        self.avg_gain = (self.avg_gain * (self.period - 1) + gain) / self.period
        self.avg_loss = (self.avg_loss * (self.period - 1) + loss) / self.period

        self.prev_price = price

        if self.avg_loss == 0:
            return 100.0

        rs = self.avg_gain / self.avg_loss
        return 100 - 100 / (1 + rs)

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

        if len(self.closes) < self.period + 3:
            return None

        rsi = self.update_rsi(price)
        if rsi is None:
            return None

        if self.prev_rsi is None:
            self.prev_rsi = rsi
            return None

        buy_cross = self.prev_rsi > self.buy_level and rsi <= self.buy_level
        sell_cross = self.prev_rsi < self.sell_level and rsi >= self.sell_level

        self.prev_rsi = rsi

        if buy_cross and self.position != "LONG":
            self.position = "LONG"
            self.cooldown_counter = self.cooldown_bars
            return "BUY"

        if sell_cross and self.position != "SHORT":
            self.position = "SHORT"
            self.cooldown_counter = self.cooldown_bars
            return "SELL"

        return None
