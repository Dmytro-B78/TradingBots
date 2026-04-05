# ================================================================
# File: bot_ai/common/utils.py
# Module: common.utils
# Purpose: NT-Tech shared utility helpers
# Responsibilities:
#   - Safe numeric parsing
#   - Rolling window helpers
#   - Basic math utilities
# Notes:
#   - ASCII-only
# ================================================================

def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def rolling_window(values, size):
    if size <= 0:
        return []
    if len(values) < size:
        return []
    return values[-size:]


def pct_change(prev, curr):
    if prev == 0:
        return 0.0
    return (curr - prev) / prev


def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))
