# ================================================================
# File: bot_ai/engine/indicators.py
# Module: engine.indicators
# Purpose: Basic technical indicators for NT-Tech engines
# Responsibilities:
#   - Compute moving averages
#   - Compute RSI
#   - Provide reusable indicator utilities
# Notes:
#   - ASCII-only
# ================================================================

class Indicators:
    """
    NT-Tech indicator utilities.
    """

    # ------------------------------------------------------------
    # Simple Moving Average
    # ------------------------------------------------------------
    @staticmethod
    def sma(values, period):
        if period <= 0 or len(values) < period:
            return None
        return sum(values[-period:]) / period

    # ------------------------------------------------------------
    # Exponential Moving Average
    # ------------------------------------------------------------
    @staticmethod
    def ema(values, period):
        if period <= 0 or len(values) < period:
            return None

        k = 2 / (period + 1)
        ema_val = values[0]

        for v in values[1:]:
            ema_val = ema_val + k * (v - ema_val)

        return ema_val

    # ------------------------------------------------------------
    # Relative Strength Index
    # ------------------------------------------------------------
    @staticmethod
    def rsi(values, period=14):
        if period <= 0 or len(values) < period + 1:
            return None

        gains = []
        losses = []

        for i in range(1, period + 1):
            diff = values[-i] - values[-i - 1]
            if diff >= 0:
                gains.append(diff)
            else:
                losses.append(-diff)

        avg_gain = sum(gains) / period if gains else 0
        avg_loss = sum(losses) / period if losses else 0

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
