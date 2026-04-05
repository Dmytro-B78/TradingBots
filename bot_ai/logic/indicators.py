# ================================================================
# File: bot_ai/logic/indicators.py
# Module: logic.indicators
# Purpose: NT-Tech indicator utilities
# Responsibilities:
#   - Moving averages
#   - RSI
#   - MACD
# Notes:
#   - ASCII-only
# ================================================================

import numpy as np


class Indicators:
    """
    NT-Tech indicator utilities.
    """

    @staticmethod
    def sma(values, period):
        if len(values) < period:
            return None
        return float(np.mean(values[-period:]))

    @staticmethod
    def ema(values, period):
        if len(values) < period:
            return None
        weights = np.exp(np.linspace(-1., 0., period))
        weights /= weights.sum()
        return float(np.dot(values[-period:], weights))

    @staticmethod
    def rsi(values, period=14):
        if len(values) < period + 1:
            return None
        deltas = np.diff(values)
        gains = deltas[deltas > 0].sum() / period
        losses = -deltas[deltas < 0].sum() / period
        if losses == 0:
            return 100.0
        rs = gains / losses
        return 100 - (100 / (1 + rs))
