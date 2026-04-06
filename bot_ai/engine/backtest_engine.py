# ================================================================
# File: bot_ai/engine/backtest_engine.py
# NT-Tech Backtest Engine 4.2 (ASCII-only)
# Deterministic backtesting engine for LiveEngine 3.1
# CSV format: open_time, open, high, low, close, volume
# ================================================================

import csv
from bot_ai.engine.live_engine import LiveEngine


class BacktestEngine:
    def __init__(self, initial_balance=10000.0):
        self.engine = LiveEngine()
        self.initial_balance = float(initial_balance)

        self.balance = float(initial_balance)
        self.equity = float(initial_balance)

        self.position = None
        self.entry_price = None
        self.position_size = 0.0

        self.equity_curve = []
        self.trades = []

        self.max_equity = float(initial_balance)
        self.max_drawdown = 0.0

    # ------------------------------------------------------------
    # Load candles from CSV (Binance-compatible, safe parsing)
    # ------------------------------------------------------------
    def load_candles(self, path):
        candles = []
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:

                # read timestamp or open_time
                ts = row.get("timestamp") or row.get("open_time")

                # skip rows without timestamp
                if ts is None or ts.strip() == "":
                    continue

                try:
                    ts_val = int(float(ts))
                except:
                    continue

                try:
                    o = float(row["open"])
                    h = float(row["high"])
                    l = float(row["low"])
                    c = float(row["close"])
                    v = float(row["volume"])
                except:
                    continue

                candles.append({
                    "timestamp": ts_val,
                    "open": o,
                    "high": h,
                    "low": l,
                    "close": c,
                    "volume": v
                })

        return candles

    # ------------------------------------------------------------
    # Compute equity
    # ------------------------------------------------------------
    def compute_equity(self, price):
        if self.position is None:
            return self.balance
        return self.balance + (price - self.entry_price) * self.position_size

    # ------------------------------------------------------------
    # Execute trade actions
    # ------------------------------------------------------------
    def handle_risk_action(self, action, price, timestamp):
        if action is None:
            return

        act = action["action"]

        if act == "OPEN_LONG" and self.position is None:
            self.position = "LONG"
            self.entry_price = price
            self.position_size = self.balance / price

            self.trades.append({
                "type": "OPEN_LONG",
                "price": price,
                "timestamp": timestamp
            })
            return

        if act.startswith("CLOSE_LONG") and self.position == "LONG":
            exit_value = self.position_size * price
            pnl = exit_value - self.balance

            self.trades.append({
                "type": act,
                "entry": self.entry_price,
                "exit": price,
                "pnl": pnl,
                "timestamp": timestamp
            })

            self.balance = exit_value
            self.position = None
            self.entry_price = None
            self.position_size = 0.0

    # ------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------
    def run(self, path):
        candles = self.load_candles(path)

        for c in candles:
            price = c["close"]
            timestamp = c["timestamp"]

            result = self.engine.on_candle(c)
            risk_action = result["risk_action"]

            self.handle_risk_action(risk_action, price, timestamp)

            self.equity = self.compute_equity(price)
            self.equity_curve.append(self.equity)

            if self.equity > self.max_equity:
                self.max_equity = self.equity

            dd = self.max_equity - self.equity
            if dd > self.max_drawdown:
                self.max_drawdown = dd

        if self.position == "LONG":
            last_price = candles[-1]["close"]
            self.handle_risk_action(
                {"action": "CLOSE_LONG_META", "price": last_price},
                last_price,
                candles[-1]["timestamp"]
            )

        return self.summary()

    # ------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------
    def summary(self):
        wins = sum(1 for t in self.trades if t.get("pnl", 0) > 0)
        losses = sum(1 for t in self.trades if t.get("pnl", 0) < 0)
        total = wins + losses

        winrate = (wins / total * 100) if total > 0 else 0.0

        return {
            "initial_balance": self.initial_balance,
            "final_balance": self.balance,
            "net_profit": self.balance - self.initial_balance,
            "trades": len(self.trades),
            "wins": wins,
            "losses": losses,
            "winrate_pct": round(winrate, 2),
            "max_drawdown": round(self.max_drawdown, 4),
            "equity_curve": self.equity_curve,
            "trade_log": self.trades
        }
