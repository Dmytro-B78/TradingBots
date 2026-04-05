# ================================================================
# File: bot_ai/execution/order_builder.py
# Module: execution.order_builder
# Purpose: NT-Tech order builder
# Responsibilities:
#   - Construct normalized order dictionaries
#   - Support MARKET, LIMIT, STOP_MARKET, STOP_LIMIT, OCO
# Notes:
#   - ASCII-only
# ================================================================

class OrderBuilder:
    """
    NT-Tech order builder.
    Produces normalized order dictionaries for execution layer.
    """

    def build(self, symbol, side, order_type, size, price=None,
              stop_price=None, limit_price=None,
              take_profit=None, stop_loss=None):

        order = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "size": float(size)
        }

        # MARKET
        if order_type.upper() == "MARKET":
            return order

        # LIMIT
        if order_type.upper() == "LIMIT":
            order["price"] = float(price)
            return order

        # STOP_MARKET
        if order_type.upper() == "STOP_MARKET":
            order["stop_price"] = float(stop_price)
            return order

        # STOP_LIMIT
        if order_type.upper() == "STOP_LIMIT":
            order["stop_price"] = float(stop_price)
            order["limit_price"] = float(limit_price)
            return order

        # OCO
        if order_type.upper() == "OCO":
            order["take_profit"] = take_profit
            order["stop_loss"] = stop_loss
            return order

        raise ValueError(f"Unsupported order type: {order_type}")
