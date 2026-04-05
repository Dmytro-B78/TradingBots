# ================================================================
# File: bot_ai/logic/signal_pipeline.py
# Module: logic.signal_pipeline
# Purpose: NT-Tech unified signal pipeline
# Responsibilities:
#   - Feed price updates into strategy
#   - Collect raw strategy signals
#   - Apply risk engine validation
#   - Produce final execution decisions
# Notes:
#   - ASCII-only
# ================================================================

class SignalPipeline:
    """
    NT-Tech unified signal pipeline.
    """

    def __init__(self, strategy, risk_engine):
        self.strategy = strategy
        self.risk_engine = risk_engine

    def update(self, price):
        self.strategy.update(price)

    def process(self, price):
        self.update(price)

        raw = self.strategy.generate()
        if not raw:
            return None

        decision = self.risk_engine.decide(raw, price)
        return decision
