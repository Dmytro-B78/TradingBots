# ================================================================
# File: bot_ai/execution/execution_router.py
# Module: execution.execution_router
# Purpose: NT-Tech execution router
# Responsibilities:
#   - Route decisions to execution manager
#   - Provide abstraction for strategy/logic layers
# Notes:
#   - ASCII-only
# ================================================================

class ExecutionRouter:
    """
    NT-Tech execution router.
    Provides a clean interface for strategy and logic layers.
    """

    def __init__(self, execution_manager):
        self.manager = execution_manager

    def route(self, decision, symbol):
        """
        decision example:
            {
                "side": "BUY",
                "type": "MARKET",
                "size": 0.01
            }
        """
        size = decision.get("size", 0)
        return self.manager.execute(decision, symbol, size)
