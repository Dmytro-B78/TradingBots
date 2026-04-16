# ================================================================
# File: analyzer.py
# NT-Tech Backtest Analyzer 2.2
# ASCII-only, deterministic, safe for pipeline integration
# ================================================================

import math
from typing import List, Dict, Any


class BacktestAnalyzer:
    """
    Analyzer 2.2
    - Processes trades
    - Processes risk snapshots
    - Builds equity curve
    - Computes drawdown, winrate, PF, avg metrics
    - Aggregates by day
    """

    def __init__(self):
        self.trades = []
        self.risk = []
        self.equity = [100.0]  # start equity
        self.kill_events = 0

    # ------------------------------------------------------------
    # Data ingestion
    # ------------------------------------------------------------
    def add_trade(self, trade: Dict[str, Any]):
        self.trades.append(trade)

    def add_risk_snapshot(self, snap: Dict[str, Any]):
        self.risk.append(snap)
        if snap.get("kill_switch_triggered"):
            self.kill_events += 1

    # ------------------------------------------------------------
    # Core metrics
    # ------------------------------------------------------------
    def compute_equity_curve(self):
        eq = 100.0
        curve = [eq]

        for t in self.trades:
            pnl = t.get("pnl", 0.0)
            eq += pnl
            curve.append(eq)

        self.equity = curve
        return curve

    def compute_drawdown(self):
        peak = -1e9
        max_dd = 0.0

        for eq in self.equity:
            if eq > peak:
                peak = eq
            dd = (eq - peak)
            if dd < max_dd:
                max_dd = dd

        return max_dd

    def compute_trade_stats(self):
        wins = [t["pnl"] for t in self.trades if t["pnl"] > 0]
        losses = [t["pnl"] for t in self.trades if t["pnl"] < 0]

        winrate = len(wins) / len(self.trades) if self.trades else 0.0
        avg_win = sum(wins) / len(wins) if wins else 0.0
        avg_loss = sum(losses) / len(losses) if losses else 0.0

        gross_profit = sum(wins)
        gross_loss = abs(sum(losses))
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else math.inf

        return {
            "trades": len(self.trades),
            "winrate": winrate,
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "profit_factor": profit_factor,
        }

    def compute_daily_aggregation(self):
        days = {}
        for t in self.trades:
            day = t.get("day", "unknown")
            pnl = t.get("pnl", 0.0)
            days.setdefault(day, 0.0)
            days[day] += pnl
        return days

    # ------------------------------------------------------------
    # Final report
    # ------------------------------------------------------------
    def build_report(self):
        self.compute_equity_curve()

        trade_stats = self.compute_trade_stats()
        max_dd = self.compute_drawdown()
        daily = self.compute_daily_aggregation()

        return {
            "equity_end": self.equity[-1] if self.equity else 100.0,
            "max_drawdown": max_dd,
            "kill_events": self.kill_events,
            "trade_stats": trade_stats,
            "daily_pnl": daily,
        }


# ------------------------------------------------------------
# Helper function for pipeline
# ------------------------------------------------------------
def analyze_backtest(trades: List[Dict[str, Any]], risk_snaps: List[Dict[str, Any]]):
    analyzer = BacktestAnalyzer()

    for t in trades:
        analyzer.add_trade(t)

    for r in risk_snaps:
        analyzer.add_risk_snapshot(r)

    return analyzer.build_report()
