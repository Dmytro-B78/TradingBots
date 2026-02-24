# ============================================
# File: C:\TradingBots\NT\bot_ai\core\signal.py
# Purpose: Signal class definition with __str__ and to_dict
# Structure: Represents a trading signal with symbol, action, price, and time
# Encoding: UTF-8 without BOM
# ============================================

class Signal:
    def __init__(self, symbol: str, action: str, price: float, time):
        self.symbol = symbol
        self.action = action
        self.price = price
        self.time = time

    def __str__(self):
        price_str = f"{self.price:.2f}" if self.price is not None else "?"
        time_str = self.time.strftime("%Y-%m-%d %H:%M:%S") if hasattr(self.time, "strftime") else str(self.time)
        return f"[SIGNAL] {self.action.upper()} {self.symbol} @ {price_str} [{time_str}]"

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "action": self.action,
            "price": self.price,
            "time": self.time
        }
