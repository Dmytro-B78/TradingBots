# ================================================================
# File: bot_ai/engine/live_engine.py
# NT-Tech LiveEngine 3.3 (ASCII-only)
# Position-synchronized engine for MetaStrategy 4.1 and RiskManager 1.2
# ================================================================

from bot_ai.strategy.meta_strategy import MetaStrategy
from bot_ai.engine.risk_manager import RiskManager

class LiveEngine:
    def __init__(self, config=None):
        self.meta = MetaStrategy()
        self.risk = RiskManager()
        self.last_action = None
    # ------------------------------------------------------------
    # Main candle handler
    # ------------------------------------------------------------
    def on_candle(self, candle):
        # meta strategy receives current position from risk manager
        meta_signal = self.meta.on_candle(
            candle=candle,
            position=self.risk.position
        )

        # risk manager receives meta decision
        risk_action = self.risk.on_candle(
            candle=candle,
            meta_signal=meta_signal
        )

        # sync position back to meta strategy
        self.meta.position = self.risk.position

        result = {
            "candle": candle,
            "meta_signal": meta_signal,
            "risk_action": risk_action,
            "position": self.risk.position
        }

        self.last_action = result
        return result
    # ------------------------------------------------------------
    # Reset engine state
    # ------------------------------------------------------------
    def reset(self):
        self.meta = MetaStrategy()
        self.risk = RiskManager()
        self.last_action = None
