# ================================================================
# File: bot_ai/engine/indicators_advanced.py
# NT-Tech IndicatorsAdvanced 3.2 (ASCII-only, deterministic)
# ================================================================

import math


class IndicatorsAdvanced:
    """
    NT-Tech optimized indicator utilities.
    Includes:
        - SMA
        - EMA
        - WMA
        - HMA
        - ATR (full + incremental)
    """

    # ------------------------------------------------------------
    # Simple Moving Average (single)
    # ------------------------------------------------------------
    @staticmethod
    def sma(values, period):
        if period <= 0 or len(values) < period:
            return None
        return sum(values[-period:]) / period

    # ------------------------------------------------------------
    # Simple Moving Average (series)
    # ------------------------------------------------------------
    @staticmethod
    def sma_series(values, period):
        n = len(values)
        if period <= 0 or n < period:
            return [None] * n

        out = [None] * n
        window_sum = sum(values[:period])
        out[period - 1] = window_sum / period

        for i in range(period, n):
            window_sum += values[i] - values[i - period]
            out[i] = window_sum / period

        return out

    # ------------------------------------------------------------
    # Exponential Moving Average (single)
    # ------------------------------------------------------------
    @staticmethod
    def ema(values, period):
        if period <= 0 or len(values) < period:
            return None

        k = 2 / (period + 1)
        ema_val = sum(values[:period]) / period

        for v in values[period:]:
            ema_val = v * k + ema_val * (1 - k)

        return ema_val

    # ------------------------------------------------------------
    # Exponential Moving Average (series)
    # ------------------------------------------------------------
    @staticmethod
    def ema_series(values, period):
        n = len(values)
        if period <= 0 or n < period:
            return [None] * n

        out = [None] * n
        k = 2 / (period + 1)

        ema_val = sum(values[:period]) / period
        out[period - 1] = ema_val

        for i in range(period, n):
            ema_val = values[i] * k + ema_val * (1 - k)
            out[i] = ema_val

        return out

    # ------------------------------------------------------------
    # Weighted Moving Average (single)
    # ------------------------------------------------------------
    @staticmethod
    def wma(values, period):
        if period <= 0 or len(values) < period:
            return None

        weights = list(range(1, period + 1))
        segment = values[-period:]

        return sum(w * v for w, v in zip(weights, segment)) / sum(weights)

    # ------------------------------------------------------------
    # Weighted Moving Average (series)
    # ------------------------------------------------------------
    @staticmethod
    def wma_series(values, period):
        n = len(values)
        if period <= 0 or n < period:
            return [None] * n

        out = [None] * n
        weights = list(range(1, period + 1))
        w_sum = sum(weights)

        for i in range(period - 1, n):
            segment = values[i - period + 1 : i + 1]
            out[i] = sum(w * v for w, v in zip(weights, segment)) / w_sum

        return out

    # ------------------------------------------------------------
    # Hull Moving Average (single)
    # ------------------------------------------------------------
    @staticmethod
    def hma(values, period):
        if period <= 0 or len(values) < period:
            return None

        half = period // 2
        sqrt_p = int(math.sqrt(period))

        wma_half = IndicatorsAdvanced.wma(values, half)
        wma_full = IndicatorsAdvanced.wma(values, period)

        if wma_half is None or wma_full is None:
            return None

        diff_series = [2 * wma_half - wma_full]

        return IndicatorsAdvanced.wma(diff_series, sqrt_p)

    # ------------------------------------------------------------
    # Hull Moving Average (series)
    # ------------------------------------------------------------
    @staticmethod
    def hma_series(values, period):
        n = len(values)
        if period <= 0 or n < period:
            return [None] * n

        half = period // 2
        sqrt_p = int(math.sqrt(period))

        wma_half = IndicatorsAdvanced.wma_series(values, half)
        wma_full = IndicatorsAdvanced.wma_series(values, period)

        diff = []
        for i in range(n):
            if wma_half[i] is None or wma_full[i] is None:
                diff.append(None)
            else:
                diff.append(2 * wma_half[i] - wma_full[i])

        return IndicatorsAdvanced.wma_series(diff, sqrt_p)

    # ============================================================
    # ATR (Average True Range)
    # ============================================================

    @staticmethod
    def tr(prev_close, high, low):
        """
        True Range:
        TR = max(
            high - low,
            abs(high - prev_close),
            abs(low - prev_close)
        )
        """
        return max(
            high - low,
            abs(high - prev_close),
            abs(low - prev_close)
        )

    @staticmethod
    def atr(candles, period):
        """
        Full ATR calculation (slow).
        Used only for initial warm-up.
        """
        if period <= 0 or len(candles) < period + 1:
            return None

        trs = []
        for i in range(1, len(candles)):
            prev_close = candles[i - 1]["close"]
            high = candles[i]["high"]
            low = candles[i]["low"]
            trs.append(IndicatorsAdvanced.tr(prev_close, high, low))

        if len(trs) < period:
            return None

        return sum(trs[-period:]) / period

    @staticmethod
    def atr_incremental(prev_atr, prev_close, high, low, period):
        """
        Incremental ATR (O(1) per candle).
        This is the correct and fast ATR for MetaStrategy 2.5.
        """
        tr = IndicatorsAdvanced.tr(prev_close, high, low)

        if prev_atr is None:
            return tr

        return (prev_atr * (period - 1) + tr) / period
