# ================================================================
# File: bot_ai/engine/risk_manager.py
# NT-Tech RiskManager Stub (deprecated)
# ASCII-only
# ================================================================

class RiskManager:
    """
    Deprecated NT-Tech RiskManager.
    Kept only for backward compatibility.
    All risk logic is now handled by:
        - MetaStrategy 2.2
        - BacktestEngine 2.2
        - LiveEngine 2.5 (Strict Mode C)
    """

    def __init__(self, params=None):
        self.params = params if isinstance(params, dict) else {}

    def stop_loss_triggered(self, entry_price, current_price):
        return False

    def take_profit_triggered(self, entry_price, current_price):
        return False

    def drawdown_triggered(self, current_equity):
        return False

    def position_allowed(self, balance, price):
        return True
