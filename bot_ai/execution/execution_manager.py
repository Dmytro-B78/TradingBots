# ================================================================
# File: bot_ai/execution/execution_manager.py
# Module: execution.execution_manager
# Purpose: NT-Tech trade execution layer
# Responsibilities:
#   - Route orders to exchange connector
#   - Normalize order requests
#   - Validate trade size and direction
#   - Return unified execution results
# Notes:
#   - ASCII-only
# ================================================================

from bot_ai.exchange.exchange_connector import ExchangeConnector
from bot_ai.utils.logger import log


class ExecutionManager:
    """
    NT-Tech execution manager.
    """

    def __init__(self, api_key, api_secret, base_url="https://api.binance.com"):
        self.connector = ExchangeConnector(api_key, api_secret, base_url)

    def execute(self, decision, symbol, size):
        if not decision:
            return {"status": "ignored", "reason": "no decision"}

        side = decision.get("side")
        if side not in ["BUY", "SELL"]:
            return {"status": "error", "reason": "invalid side"}

        try:
            if side == "BUY":
                result = self.connector.order_market(symbol, "BUY", size)
            else:
                result = self.connector.order_market(symbol, "SELL", size)

            return {
                "status": "ok",
                "order": result
            }

        except Exception as e:
            log.error(f"Execution error: {e}")
            return {
                "status": "error",
                "reason": str(e)
            }
