# ================================================================
# File: bot_ai/logic/candle_math.py
# Module: logic.candle_math
# Purpose: NT-Tech candle utilities
# Responsibilities:
#   - Candle body size
#   - Wick size
#   - Volatility metrics
# Notes:
#   - ASCII-only
# ================================================================

class CandleMath:
    """
    NT-Tech candle math utilities.
    """

    @staticmethod
    def body(candle):
        return abs(candle["close"] - candle["open"])

    @staticmethod
    def wick_top(candle):
        return candle["high"] - max(candle["open"], candle["close"])

    @staticmethod
    def wick_bottom(candle):
        return min(candle["open"], candle["close"]) - candle["low"]

    @staticmethod
    def range(candle):
        return candle["high"] - candle["low"]
