# ================================================================
# File: bot_ai/execution/order_executor.py
# Module: execution.order_executor
# Purpose: NT-Tech order executor
# Responsibilities:
#   - High-level wrapper around exchange adapter
#   - Provide clean API for placing and managing orders
# Notes:
#   - ASCII-only
# ================================================================

from bot_ai.execution.execution_errors import ExecutionError
from bot_ai.execution.order_status import OrderStatus


class OrderExecutor:
    """
    NT-Tech order executor.
    Wraps exchange adapter and returns normalized results.
    """

    def __init__(self, adapter):
        self.adapter = adapter

    def place(self, order):
        try:
            data = self.adapter.send_order(order)
            return data
        except Exception as e:
            raise ExecutionError(str(e))

    def status(self, order_id, symbol):
        try:
            data = self.adapter.get_order_status(order_id, symbol)
            return OrderStatus(
                status=data["status"],
                filled=data["filled"],
                remaining=data["remaining"],
                raw=data["raw"]
            )
        except Exception as e:
            raise ExecutionError(str(e))

    def cancel(self, order_id, symbol):
        try:
            data = self.adapter.cancel_order(order_id, symbol)
            return data
        except Exception as e:
            raise ExecutionError(str(e))
