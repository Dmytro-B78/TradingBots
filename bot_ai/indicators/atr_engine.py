# ================================================================
# File: bot_ai/indicators/atr_engine.py
# NT-Tech ATR Engine 1.0
# - Deterministic ATR(14/21) for any timeframe
# - ATR slope, ATR ratio, ATR compression
# - ATR regime classification (low / normal / high / extreme)
# ================================================================

class ATREngine:
    """
    Classic Wilder ATR engine.
    Works with any timeframe (1h, 4h, etc).
    """

    def __init__(self, period=14):
        self.period = period
        self.buffer = []          # raw candles
        self.atr = None           # last ATR value
        self.prev_atr = None      # for slope

    # ------------------------------------------------------------
    # Update ATR on new candle
    # ------------------------------------------------------------
    def on_candle(self, candle):
        """
        candle = {open, high, low, close}
        Returns ATR or None if not enough data.
        """

        self.buffer.append(candle)
        if len(self.buffer) < self.period + 1:
            return None

        # Compute TR series
        trs = []
        prev_close = self.buffer[-(self.period + 1)]["close"]

        for c in self.buffer[-self.period:]:
            h = c["high"]
            l = c["low"]
            tr = max(h - l, abs(h - prev_close), abs(l - prev_close))
            trs.append(tr)
            prev_close = c["close"]

        # Wilder ATR
        self.prev_atr = self.atr
        self.atr = sum(trs) / float(self.period)

        return self.atr

    # ------------------------------------------------------------
    # ATR slope (direction of volatility)
    # ------------------------------------------------------------
    def get_slope(self):
        if self.atr is None or self.prev_atr is None:
            return 0.0
        return self.atr - self.prev_atr

    # ------------------------------------------------------------
    # ATR compression (volatility squeeze)
    # ------------------------------------------------------------
    def is_compressing(self, threshold=0.0):
        """
        Returns True if ATR is shrinking.
        threshold = minimal slope to consider compression.
        """
        slope = self.get_slope()
        return slope < threshold

    # ------------------------------------------------------------
    # ATR ratio (for multi-TF ATR)
    # ------------------------------------------------------------
    @staticmethod
    def ratio(atr_fast, atr_slow):
        if atr_fast is None or atr_slow is None or atr_slow == 0:
            return None
        return atr_fast / atr_slow


# ================================================================
# ATR Regime Classifier
# ================================================================

class ATRRegime:
    """
    Classifies ATR into volatility regimes:
      - low
      - normal
      - high
      - extreme
    Based on ATR percentage relative to price.
    """

    def __init__(self, low_pct=0.002, high_pct=0.015, extreme_pct=0.030):
        self.low_pct = low_pct
        self.high_pct = high_pct
        self.extreme_pct = extreme_pct

    def classify(self, atr_value, price):
        if atr_value is None or price <= 0:
            return "unknown"

        atr_pct = atr_value / price

        if atr_pct <= self.low_pct:
            return "low"
        if atr_pct <= self.high_pct:
            return "normal"
        if atr_pct <= self.extreme_pct:
            return "high"
        return "extreme"
