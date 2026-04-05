# ================================================================
# File: bot_ai/logic/risk_engine.py
# Module: logic.risk_engine
# Purpose: NT-Tech risk management engine
# Responsibilities:
#   - Enforce max position limits
#   - Validate signal direction
#   - Normalize trade size
#   - Block trades in unsafe conditions
# Notes:
#   - ASCII-only
# ================================================================

class RiskEngine:
    """
    NT-Tech risk engine.
    """

    def __init__(self, max_position=1.0):
        self.max_position = max_position
        self.current_position = 0.0

    def decide(self, signal, price):
        if not signal:
            return None

        direction = signal.get("signal", 0)
        if direction == 0:
            return None

        if direction > 0 and self.current_position >= self.max_position:
            return None

        if direction < 0 and self.current_position <= -self.max_position:
            return None

        size = 1.0

        if direction > 0:
            self.current_position += size
            return {"side": "BUY", "size": size}

        if direction < 0:
            self.current_position -= size
            return {"side": "SELL", "size": size}

        return None
