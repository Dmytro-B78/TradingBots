# ================================================================
# File: bot_ai/engine/order_engine.py
# NT-Tech order execution engine (extended)
# ASCII-only
# ================================================================

class OrderEngine:
    """
    NT-Tech order execution engine supporting:
        - long and short positions
        - commission fees
        - unified open/close interface
        - PnL calculation
        - trade history tracking
    """

    def __init__(self, fee_rate=0.001):
        self.fee_rate = float(fee_rate)
        self.balance = 0.0
        self.position = 0.0
        self.entry_price = None
        self.trades = []

    # ------------------------------------------------------------
    # Set initial balance
    # ------------------------------------------------------------
    def set_initial_balance(self, amount):
        try:
            self.balance = float(amount)
        except Exception:
            self.balance = 0.0

    # ------------------------------------------------------------
    # BUY wrapper (long open)
    # ------------------------------------------------------------
    def buy(self, price):
        return self.open(1.0, price)

    # ------------------------------------------------------------
    # SELL wrapper (long close)
    # ------------------------------------------------------------
    def sell(self, price):
        return self.close(price)

    # ------------------------------------------------------------
    # Open a position (long or short)
    # size > 0 => long
    # size < 0 => short
    # ------------------------------------------------------------
    def open(self, size, price):
        if size == 0:
            return None

        if self.position != 0:
            return None

        try:
            qty = float(size)
            p = float(price)
        except Exception:
            return None

        cost = abs(qty) * p
        fee = cost * self.fee_rate

        if qty > 0:
            total = cost + fee
            if total > self.balance:
                return None
            self.balance -= total
        else:
            net = cost - fee
            self.balance += net

        self.position = qty
        self.entry_price = p

        trade = {
            "type": "OPEN_LONG" if qty > 0 else "OPEN_SHORT",
            "price": p,
            "qty": qty
        }
        self.trades.append(trade)
        return trade

    # ------------------------------------------------------------
    # Close current position
    # ------------------------------------------------------------
    def close(self, price):
        if self.position == 0:
            return 0.0

        try:
            p = float(price)
        except Exception:
            return 0.0

        qty = self.position
        cost = abs(qty) * p
        fee = cost * self.fee_rate

        if qty > 0:
            net = cost - fee
            self.balance += net
        else:
            total = cost + fee
            self.balance -= total

        pnl = (p - self.entry_price) * qty

        trade = {
            "type": "CLOSE_LONG" if qty > 0 else "CLOSE_SHORT",
            "price": p,
            "qty": qty,
            "pnl": pnl
        }
        self.trades.append(trade)

        self.position = 0.0
        self.entry_price = None

        return pnl

    # ------------------------------------------------------------
    # Current equity including open position
    # ------------------------------------------------------------
    def equity(self, price):
        try:
            p = float(price)
        except Exception:
            return self.balance

        if self.position == 0:
            return self.balance

        pnl = (p - self.entry_price) * self.position
        return self.balance + pnl

    # ------------------------------------------------------------
    # Trade history
    # ------------------------------------------------------------
    def get_trades(self):
        return self.trades
