# ================================================================
# File: bot_ai/common/indicators.py
# Module: common.indicators
# Purpose: NT-Tech technical indicator utilities
# Responsibilities:
#   - Compute SMA, EMA
#   - Compute RSI
#   - Compute Bollinger Bands
#   - Provide reusable math helpers for strategies
# Notes:
#   - ASCII-only
# ================================================================

import statistics


def sma(values, period):
    if len(values) < period:
        return None
    return sum(values[-period:]) / period


def ema(values, period):
    if len(values) < period:
        return None
    k = 2 / (period + 1)
    ema_val = values[0]
    for v in values[1:]:
        ema_val = v * k + ema_val * (1 - k)
    return ema_val


def rsi(values, period=14):
    if len(values) < period + 1:
        return None

    gains = []
    losses = []

    for i in range(1, period + 1):
        diff = values[-i] - values[-i - 1]
        if diff > 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))

    avg_gain = sum(gains) / period if gains else 0
    avg_loss = sum(losses) / period if losses else 0

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def bollinger(values, period=20, deviation=2.0):
    if len(values) < period:
        return None, None, None

    window = values[-period:]
    sma_val = sum(window) / period
    std = statistics.pstdev(window)

    upper = sma_val + deviation * std
    lower = sma_val - deviation * std

    return lower, sma_val, upper
