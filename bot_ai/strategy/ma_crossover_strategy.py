# ================================================================
# File: bot_ai/strategy/ma_crossover_strategy.py
# NT-Tech MA Crossover Strategy 3.1 (no ATR filter)
# ASCII-only
# ================================================================

from bot_ai.engine.indicators_advanced import IndicatorsAdvanced


class MACrossoverStrategy:
    """
    NT-Tech MA Crossover Strategy 3.1
    - incremental MA
    - no ATR filter (handled by MetaStrategy)
    - no trend filter (handled by MetaStrategy)
    - O(1) per candle
    """

    def __init__(self, params=None):
        self.params = params if isinstance(params, dict) else {}

        self.short_period = self.params.get("short", 9)
        self.long_period = self.params.get("long", 21)
        self.ma_type = self.params.get("type", "EMA")

        self.cooldown_bars = self.params.get("cooldown", 3)
        self.cooldown_counter = 0

        self.position = "FLAT"
        self.closes = []

        self.short_ma = None
        self.long_ma = None

        self.prev_short = None
        self.prev_long = None

        self.k_short = 2 / (self.short_period + 1)
        self.k_long = 2 / (self.long_period + 1)

    # ------------------------------------------------------------
    # Incremental MA update
    # ------------------------------------------------------------
    def update_ma(self, price):
        if self.ma_type == "EMA":
            if self.short_ma is None:
                self.short_ma = price
            else:
                self.short_ma = price * self.k_short + self.short_ma * (1 - self.k_short)

            if self.long_ma is None:
                self.long_ma = price
            else:
                self.long_ma = price * self.k_long + self.long_ma * (1 - self.k_long)

            return self.short_ma, self.long_ma

        # SMA fallback
        if len(self.closes) >= self.short_period:
            if self.short_ma is None:
                self.short_ma = sum(self.closes[-self.short_period:]) / self.short_period
            else:
                self.short_ma += (price - self.closes[-self.short_period]) / self.short_period

        if len(self.closes) >= self.long_period:
            if self.long_ma is None:
                self.long_ma = sum(self.closes[-self.long_period:]) / self.long_period
            else:
                self.long_ma += (price - self.closes[-self.long_period]) / self.long_period

        return self.short_ma, self.long_ma

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

        if len(self.closes) < self.long_period + 3:
            return None

        short_ma, long_ma = self.update_ma(price)
        if short_ma is None or long_ma is None:
            return None

        if self.prev_short is None:
            self.prev_short = short_ma
            self.prev_long = long_ma
            return None

        buy_cross = self.prev_short <= self.prev_long and short_ma > long_ma
        sell_cross = self.prev_short >= self.prev_long and short_ma < long_ma

        self.prev_short = short_ma
        self.prev_long = long_ma

        if buy_cross and self.position != "LONG":
            self.position = "LONG"
            self.cooldown_counter = self.cooldown_bars
            return "BUY"

        if sell_cross and self.position != "SHORT":
            self.position = "SHORT"
            self.cooldown_counter = self.cooldown_bars
            return "SELL"

        return None
