# ============================================
# File: C:\TradingBots\NT\bot_ai\strategy\signal.py
# Purpose: Signal object used by strategies
# Encoding: UTF-8 without BOM
# ============================================

class Signal:
    def __init__(self, action: str, price: float, timestamp):
        self.action = action
        self.price = price
        self.timestamp = timestamp

    def __repr__(self):
        return f"[SIGNAL] {self.action.upper()} @ {self.price} [{self.timestamp}]"
