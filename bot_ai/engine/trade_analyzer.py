# ================================================================
# File: bot_ai/engine/trade_analyzer.py
# NT-Tech TradeAnalyzer 3.1 (ASCII-only)
# Deterministic analytics for MetaStrategy 3.0 + SignalLogger 1.0
# ================================================================

import os


class TradeAnalyzer:
    """
    NT-Tech TradeAnalyzer 3.1
    - ASCII-only
    - deterministic analytics
    - O(1) per log line
    - builds:
        * equity curve
        * winrate
        * max drawdown
        * profit factor
        * expectancy
        * stats per regime
        * stats per strategy
    """

    def __init__(self, log_path="C:/TradingBots/NT/logs/signal_log.txt"):
        self.log_path = log_path

        # Equity tracking
        self.equity = 10000.0
        self.equity_curve = []

        # Trade tracking
        self.open_price = None
        self.closed_trades = []

        # Regime stats
        self.regime_stats = {}

        # Strategy stats
        self.strategy_stats = {}

    # ------------------------------------------------------------
    # Safe float conversion
    # ------------------------------------------------------------
    def to_float(self, x):
        try:
            return float(x)
        except:
            return 0.0

    # ------------------------------------------------------------
    # Parse a single log block
    # ------------------------------------------------------------
    def parse_block(self, block):
        data = {
            "open_time": None,
            "price": None,
            "regime": None,
            "decision": None,
            "strategies": [],
        }

        for line in block:
            line = line.strip()

            if line.startswith("open_time:"):
                data["open_time"] = int(line.split(":", 1)[1].strip())

            elif line.startswith("price:"):
                data["price"] = self.to_float(line.split(":", 1)[1].strip())

            elif line.startswith("regime:"):
                data["regime"] = line.split(":", 1)[1].strip()

            elif line.startswith("decision:"):
                data["decision"] = line.split(":", 1)[1].strip()

            elif ":" in line and "signal=" in line:
                # Example: MACDStrategy: signal=BUY, conf=1.0
                name, rest = line.split(":", 1)
                rest = rest.strip()
                parts = rest.split(",")
                sig = parts[0].split("=")[1].strip()
                conf = self.to_float(parts[1].split("=")[1].strip())
                data["strategies"].append((name.strip(), sig, conf))

        return data

    # ------------------------------------------------------------
    # Update regime stats
    # ------------------------------------------------------------
    def update_regime_stats(self, regime, pnl):
        if regime not in self.regime_stats:
            self.regime_stats[regime] = {
                "trades": 0,
                "wins": 0,
                "losses": 0,
                "pnl": 0.0,
            }

        rs = self.regime_stats[regime]
        rs["trades"] += 1
        rs["pnl"] += pnl

        if pnl > 0:
            rs["wins"] += 1
        else:
            rs["losses"] += 1

    # ------------------------------------------------------------
    # Update strategy stats
    # ------------------------------------------------------------
    def update_strategy_stats(self, strategies, pnl):
        for name, sig, conf in strategies:
            if name not in self.strategy_stats:
                self.strategy_stats[name] = {
                    "signals": 0,
                    "pnl": 0.0,
                }

            self.strategy_stats[name]["signals"] += 1
            self.strategy_stats[name]["pnl"] += pnl

    # ------------------------------------------------------------
    # Process a parsed block
    # ------------------------------------------------------------
    def process(self, data):
        price = data["price"]
        regime = data["regime"]
        decision = data["decision"]

        if decision == "OPEN_LONG":
            self.open_price = price

        elif decision == "CLOSE_LONG" and self.open_price is not None:
            pnl = price - self.open_price
            self.equity += pnl
            self.equity_curve.append(self.equity)

            self.closed_trades.append(pnl)

            self.update_regime_stats(regime, pnl)
            self.update_strategy_stats(data["strategies"], pnl)

            self.open_price = None

    # ------------------------------------------------------------
    # Compute final metrics
    # ------------------------------------------------------------
    def compute_metrics(self):
        if not self.closed_trades:
            return {
                "equity": self.equity,
                "trades": 0,
                "wins": 0,
                "losses": 0,
                "winrate": 0.0,
                "max_drawdown": 0.0,
                "profit_factor": 0.0,
                "expectancy": 0.0,
                "regime_stats": self.regime_stats,
                "strategy_stats": self.strategy_stats,
            }

        wins = sum(1 for x in self.closed_trades if x > 0)
        losses = sum(1 for x in self.closed_trades if x <= 0)

        winrate = wins / len(self.closed_trades)

        # Max drawdown
        peak = self.equity_curve[0]
        max_dd = 0.0
        for eq in self.equity_curve:
            if eq > peak:
                peak = eq
            dd = peak - eq
            if dd > max_dd:
                max_dd = dd

        # Profit factor
        gross_profit = sum(x for x in self.closed_trades if x > 0)
        gross_loss = abs(sum(x for x in self.closed_trades if x <= 0))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0.0

        # Expectancy
        expectancy = sum(self.closed_trades) / len(self.closed_trades)

        return {
            "equity": self.equity,
            "trades": len(self.closed_trades),
            "wins": wins,
            "losses": losses,
            "winrate": winrate,
            "max_drawdown": max_dd,
            "profit_factor": profit_factor,
            "expectancy": expectancy,
            "regime_stats": self.regime_stats,
            "strategy_stats": self.strategy_stats,
        }

    # ------------------------------------------------------------
    # Run analyzer
    # ------------------------------------------------------------
    def run(self):
        if not os.path.exists(self.log_path):
            return None

        block = []

        with open(self.log_path, "r", encoding="ascii", errors="ignore") as f:
            for line in f:
                if line.startswith("------------------------------------------------------------"):
                    if block:
                        data = self.parse_block(block)
                        self.process(data)
                        block = []
                else:
                    block.append(line)

        # Process last block
        if block:
            data = self.parse_block(block)
            self.process(data)

        return self.compute_metrics()
