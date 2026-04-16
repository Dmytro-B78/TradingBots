# ================================================================
# File: bot_ai/data/mtf_aggregator.py
# NT-Tech MTF Aggregator 1.0
# - Deterministic 1h and 4h aggregation
# - No time-based guessing, only candle counting
# - Works with any base timeframe (5m, 15m, 1h)
# - Produces clean OHLCV for 1h and 4h
# ================================================================

class MTFAggregator:
    """
    Deterministic multi-timeframe aggregator.
    Converts base candles (e.g., 5m) into:
      - 1h candles (12×5m or 4×15m)
      - 4h candles (4×1h)
    """

    def __init__(self, base_tf_minutes):
        self.base_tf = base_tf_minutes

        # 1h = 60 minutes
        self.candles_per_1h = 60 // base_tf_minutes

        # 4h = 240 minutes
        self.candles_per_4h = 240 // base_tf_minutes

        # Buffers
        self.buf_1h = []
        self.buf_4h = []

        # Last completed candles
        self.last_1h = None
        self.last_4h = None

    # ------------------------------------------------------------
    # Utility: aggregate buffer into OHLCV candle
    # ------------------------------------------------------------
    def _aggregate(self, buf):
        o = buf[0]["open"]
        h = max(c["high"] for c in buf)
        l = min(c["low"] for c in buf)
        c = buf[-1]["close"]
        v = sum(c["volume"] for c in buf)
        return {"open": o, "high": h, "low": l, "close": c, "volume": v}

    # ------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------
    def on_candle(self, candle):
        """
        Input: base candle (5m/15m/1h)
        Output: (new_1h_candle or None, new_4h_candle or None)
        """

        # --- 1h aggregation ---
        self.buf_1h.append(candle)

        new_1h = None
        new_4h = None

        if len(self.buf_1h) == self.candles_per_1h:
            new_1h = self._aggregate(self.buf_1h)
            self.last_1h = new_1h
            self.buf_1h.clear()

            # 4h aggregation uses 1h candles
            self.buf_4h.append(new_1h)

            if len(self.buf_4h) == 4:
                new_4h = self._aggregate(self.buf_4h)
                self.last_4h = new_4h
                self.buf_4h.clear()

        return new_1h, new_4h
