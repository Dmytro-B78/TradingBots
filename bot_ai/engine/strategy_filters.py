# ================================================================
# File: bot_ai/engine/strategy_filters.py
# NT-Tech strategy filters (optimized)
# ASCII-only
# ================================================================

import math


class StrategyFilters:
    """
    NT-Tech optimized filters:
        - RSI series
        - ATR series
        - Trend slope series
    All filters operate in linear time for millions of candles.
    """

    # ------------------------------------------------------------
    # RSI (series)
    # ------------------------------------------------------------
    @staticmethod
    def rsi_series(values, period):
        n = len(values)
        if period <= 0 or n < period + 1:
            return [None] * n

        out = [None] * n

        gains = 0.0
        losses = 0.0

        for i in range(1, period + 1):
            diff = values[i] - values[i - 1]
            if diff >= 0:
                gains += diff
            else:
                losses -= diff

        avg_gain = gains / period
        avg_loss = losses / period

        if avg_loss == 0:
            out[period] = 100.0
        else:
            rs = avg_gain / avg_loss
            out[period] = 100.0 - (100.0 / (1.0 + rs))

        for i in range(period + 1, n):
            diff = values[i] - values[i - 1]

            gain = diff if diff > 0 else 0.0
            loss = -diff if diff < 0 else 0.0

            avg_gain = (avg_gain * (period - 1) + gain) / period
            avg_loss = (avg_loss * (period - 1) + loss) / period

            if avg_loss == 0:
                out[i] = 100.0
            else:
                rs = avg_gain / avg_loss
                out[i] = 100.0 - (100.0 / (1.0 + rs))

        return out

    # ------------------------------------------------------------
    # ATR (series)
    # ------------------------------------------------------------
    @staticmethod
    def atr_series(candles, period):
        n = len(candles)
        if period <= 0 or n < period + 1:
            return [None] * n

        out = [None] * n
        trs = [0.0] * n

        for i in range(1, n):
            high = candles[i]["high"]
            low = candles[i]["low"]
            prev_close = candles[i - 1]["close"]

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            trs[i] = tr

        atr = sum(trs[1:period + 1]) / period
        out[period] = atr

        for i in range(period + 1, n):
            atr = (atr * (period - 1) + trs[i]) / period
            out[i] = atr

        return out

    # ------------------------------------------------------------
    # Trend slope (series)
    # ------------------------------------------------------------
    @staticmethod
    def trend_series(values, period):
        n = len(values)
        if period <= 0 or n < period:
            return [None] * n

        out = [None] * n

        for i in range(period - 1, n):
            start = values[i - period + 1]
            end = values[i]
            slope = (end - start) / period
            out[i] = slope

        return out
