# ================================================================
# File: bot_ai/logic/signal_filters.py
# Module: logic.signal_filters
# Purpose: NT-Tech signal filters
# Responsibilities:
#   - Filter weak signals
#   - Prevent noise trades
# Notes:
#   - ASCII-only
# ================================================================

class SignalFilters:
    """
    NT-Tech signal filters.
    """

    def __init__(self, min_strength=0.2):
        self.min_strength = min_strength

    def passes_strength(self, signal):
        return signal.get("strength", 0) >= self.min_strength
