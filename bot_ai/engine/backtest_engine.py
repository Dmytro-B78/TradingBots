# ================================================================
# File: bot_ai/engine/backtest_engine.py
# NT-Tech Backtest Engine 3.0 (Spot-only, MetaStrategy 2.2)
# ASCII-only
# ================================================================

import math
from bot_ai.strategy.meta_strategy import MetaStrategy


class BacktestEngine:
    """
    NT-Tech Backtest Engine 3.0
    Spot-only:
        - only OPEN_LONG / CLOSE_LONG
        - ATR-based SL/TP handled by MetaStrategy
        - no short positions
        - no OrderEngine
        - no RiskManager
    """

    def __init__(self, config, candles):
        self.config = config
        self.candles = candles if isinstance(candles, list) else []

        # MetaStrategy receives full config
        self.meta = MetaStrategy(config)

        # initial balance from config
        self.balance = float(config.get("initial_balance", 10000.0))

        self.position = "FLAT"
        self.entry_price = None
        self.position_size = 0.0

        self.equity_curve = []
        self.trades = []

    # ------------------------------------------------------------
    # Equity calculation
    # ------------------------------------------------------------
    def compute_equity(self, price):
        if self.position == "FLAT":
            return self.balance
        return self.balance + (price - self.entry_price) * self.position_size

    # ------------------------------------------------------------
    # Trade execution
    # ------------------------------------------------------------
    def open_long(self, price):
        if price <= 0:
            return
        self.position = "LONG"
        self.entry_price = price
        self.position_size = self.balance / price

    def close_long(self, price, reason):
        if self.position != "LONG":
            return

        exit_value = self.position_size * price
        pnl = exit_value - self.balance

        self.trades.append({
            "entry": self.entry_price,
            "exit": price,
            "pnl": pnl,
            "reason": str(reason).encode("ascii", errors="ignore").decode("ascii")
        })

        self.balance = exit_value
        self.position = "FLAT"
        self.entry_price = None
        self.position_size = 0.0

    # ------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------
    def run(self):
        # deterministic ordering
        try:
            self.candles.sort(key=lambda x: x["open_time"])
        except Exception:
            pass

        for candle in self.candles:
            price = candle.get("close", 0.0)
            try:
                price = float(price)
            except Exception:
                continue

            signal = self.meta.on_candle(candle)

            if signal is not None:
                sig = signal.get("signal")

                if sig == "OPEN_LONG" and self.position == "FLAT":
                    self.open_long(price)

                elif sig == "CLOSE_LONG" and self.position == "LONG":
                    self.close_long(price, signal.get("reason"))

            self.equity_curve.append(self.compute_equity(price))

        # Close open position at end
        if self.position == "LONG":
            last_price = self.candles[-1]["close"]
            self.close_long(last_price, "end_of_data")

        return self.metrics()

    # ------------------------------------------------------------
    # Metrics
    # ------------------------------------------------------------
    def metrics(self):
        if not self.trades:
            return {
                "net_profit": 0.0,
                "winrate_pct": 0.0,
                "sharpe": 0.0,
                "max_drawdown": 0.0,
                "trades": 0
            }

        initial_balance = float(self.config.get("initial_balance", 10000.0))
        net_profit = self.balance - initial_balance

        wins = sum(1 for t in self.trades if t["pnl"] > 0)
        winrate = (wins / len(self.trades)) * 100.0

        returns = []
        for i in range(1, len(self.equity_curve)):
            prev = self.equity_curve[i - 1]
            curr = self.equity_curve[i]
            if prev > 0:
                returns.append((curr - prev) / prev)

        if len(returns) > 1:
            mean_r = sum(returns) / len(returns)
            std_r = math.sqrt(sum((r - mean_r) ** 2 for r in returns) / len(returns))
            sharpe = (mean_r / std_r) * math.sqrt(252) if std_r > 0 else 0.0
        else:
            sharpe = 0.0

        peak = -1e9
        max_dd = 0.0
        for eq in self.equity_curve:
            if eq > peak:
                peak = eq
            dd = (peak - eq) / peak if peak > 0 else 0.0
            if dd > max_dd:
                max_dd = dd

        return {
            "net_profit": round(net_profit, 2),
            "winrate_pct": round(winrate, 2),
            "sharpe": round(sharpe, 4),
            "max_drawdown": round(max_dd, 4),
            "trades": len(self.trades)
        }
