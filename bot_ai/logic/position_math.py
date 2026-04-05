# ================================================================
# File: bot_ai/logic/position_math.py
# Module: logic.position_math
# Purpose: NT-Tech position utilities
# Responsibilities:
#   - PnL calculations
#   - Position metrics
# Notes:
#   - ASCII-only
# ================================================================

class PositionMath:
    """
    NT-Tech position math utilities.
    """

    @staticmethod
    def pnl(entry, exit, size):
        return (exit - entry) * size

    @staticmethod
    def pnl_pct(entry, exit):
        return (exit - entry) / entry * 100.0
