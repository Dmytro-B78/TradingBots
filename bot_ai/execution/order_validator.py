# ================================================================
# File: bot_ai/execution/order_validator.py
# Module: execution.order_validator
# Purpose: NT-Tech order validator
# Responsibilities:
#   - Validate order structure
#   - Validate required fields per order type
# Notes:
#   - ASCII-only
# ================================================================

from bot_ai.execution.execution_errors import ExecutionError


class OrderValidator:
    """
    NT-Tech order validator.
    Ensures order dictionaries contain required fields.
    """

    def validate(self, order):
        if "symbol" not in order:
            raise ExecutionError("Order missing symbol")

        if "side" not in order:
            raise ExecutionError("Order missing side")

        if "type" not in order:
            raise ExecutionError("Order missing type")

        if "size" not in order or order["size"] <= 0:
            raise ExecutionError("Order size must be > 0")

        order_type = order["type"]

        # LIMIT
        if order_type == "LIMIT":
            if "price" not in order:
                raise ExecutionError("LIMIT order missing price")

        # STOP_MARKET
        if order_type == "STOP_MARKET":
            if "stop_price" not in order:
                raise ExecutionError("STOP_MARKET order missing stop_price")

        # STOP_LIMIT
        if order_type == "STOP_LIMIT":
            if "stop_price" not in order or "limit_price" not in order:
                raise ExecutionError("STOP_LIMIT order missing stop_price or limit_price")

        # OCO
        if order_type == "OCO":
            if "take_profit" not in order or "stop_loss" not in order:
                raise ExecutionError("OCO order missing take_profit or stop_loss")

        return True
