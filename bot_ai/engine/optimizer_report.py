# ================================================================
# File: bot_ai/engine/optimizer_report.py
# Module: engine.optimizer_report
# Purpose: NT-Tech optimizer reporting utilities
# Responsibilities:
#   - Format optimization results
#   - Compute summary statistics
#   - Produce structured report objects
#   - Support ranking and comparison of parameter sets
# Notes:
#   - ASCII-only
# ================================================================

class OptimizerReport:
    """
    NT-Tech optimizer report generator.
    """

    def __init__(self, results):
        self.results = results

    def summarize(self):
        summary = {
            "total_runs": len(self.results),
            "best_by_net_profit": None,
            "best_by_sharpe": None,
            "best_by_winrate": None
        }

        if not self.results:
            return summary

        summary["best_by_net_profit"] = max(
            self.results,
            key=lambda r: r["result"].get("net_profit", 0)
        )

        summary["best_by_sharpe"] = max(
            self.results,
            key=lambda r: r["result"].get("sharpe", 0)
        )

        summary["best_by_winrate"] = max(
            self.results,
            key=lambda r: r["result"].get("winrate", 0)
        )

        return summary

    def rank(self, metric="net_profit", reverse=True):
        if not self.results:
            return []

        return sorted(
            self.results,
            key=lambda r: r["result"].get(metric, 0),
            reverse=reverse
        )

    def top(self, n=5, metric="net_profit"):
        ranked = self.rank(metric=metric)
        return ranked[:n]
