# ================================================================
# File: bot_ai/strategy/macd_strategy.py
# NT-Tech MACD Strategy 3.1 (no ATR/trend filters)
# ASCII-only
# ================================================================

class MACDStrategy:
    """
    NT-Tech MACD Strategy 3.1
    - incremental MACD (fast, slow, signal)
    - no ATR filter (handled by MetaStrategy)
    - no trend filter (handled by MetaStrategy)
    - O(1) per candle
    """

    def __init__(self, params=None):
        self.params = params if isinstance(params, dict) else {}

        self.fast = self.params.get("fast", 12)
        self.slow = self.params.get("slow", 26)
        self.signal_period = self.params.get("signal", 9)

        self.cooldown_bars = self.params.get("cooldown", 3)
        self.cooldown_counter = 0

        self.position = "FLAT"
        self.closes = []

        # Incremental EMA state
        self.ema_fast = None
        self.ema_slow = None
        self.signal_line = None
        self.prev_hist = None

        # Smoothing constants
        self.k_fast = 2 / (self.fast + 1)
        self.k_slow = 2 / (self.slow + 1)
        self.k_signal = 2 / (self.signal_period + 1)

    # ------------------------------------------------------------
    # Incremental MACD update
    # ------------------------------------------------------------
    def update_macd(self, price):
        if self.ema_fast is None:
            self.ema_fast = price
            return None, None, None

        if self.ema_slow is None:
            self.ema_slow = price
            return None, None, None

        # Update EMAs
        self.ema_fast = price * self.k_fast + self.ema_fast * (1 - self.k_fast)
        self.ema_slow = price * self.k_slow + self.ema_slow * (1 - self.k_slow)

        macd_line = self.ema_fast - self.ema_slow

        if self.signal_line is None:
            self.signal_line = macd_line
            return None, None, None

        self.signal_line = (
            macd_line * self.k_signal + self.signal_line * (1 - self.k_signal)
        )

        hist = macd_line - self.signal_line
        return macd_line, self.signal_line, hist

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

        if len(self.closes) < self.slow + 5:
            return None

        macd_line, signal_line, hist = self.update_macd(price)
        if macd_line is None or signal_line is None or hist is None:
            return None

        if self.prev_hist is None:
            self.prev_hist = hist
            return None

        buy_cross = self.prev_hist <= 0 and hist > 0
        sell_cross = self.prev_hist >= 0 and hist < 0

        self.prev_hist = hist

        if buy_cross and self.position != "LONG":
            self.position = "LONG"
            self.cooldown_counter = self.cooldown_bars
            return "BUY"

        if sell_cross and self.position != "SHORT":
            self.position = "SHORT"
            self.cooldown_counter = self.cooldown_bars
            return "SELL"

        return None
