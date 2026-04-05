# ================================================================
# File: bot_ai/execution/order_status.py
# Module: execution.order_status
# Purpose: NT-Tech order status normalization
# Responsibilities:
#   - Normalize exchange order status into unified NT format
# Notes:
#   - ASCII-only
# ================================================================

class OrderStatus:
    """
    NT-Tech unified order status object.
    """

    def __init__(self, status, filled, remaining, raw):
        self.status = status
        self.filled = filled
        self.remaining = remaining
        self.raw = raw

    def is_open(self):
        return self.status in ("NEW", "PARTIAL")

    def is_filled(self):
        return self.status == "FILLED"

    def is_closed(self):
        return self.status in ("FILLED", "CANCELLED", "REJECTED")
