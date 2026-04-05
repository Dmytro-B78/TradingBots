# ================================================================
# File: bot_ai/engine/trade_analyzer.py
# NT-Tech TradeAnalyzer 3.0 (ASCII-only, deterministic)
# ================================================================

class TradeAnalyzer:

    def __init__(self, trades, initial_balance, final_value):
        self.trades = trades if isinstance(trades, list) else []
        self.initial_balance = float(initial_balance)
        self.final_value = float(final_value)

    # ------------------------------------------------------------
    # Summary statistics
    # ------------------------------------------------------------
    def summary(self):
        # deterministic ordering
        try:
            self.trades.sort(key=lambda x: x.get("time", 0))
        except Exception:
            pass

        total = len(self.trades)

        wins = 0
        losses = 0
        breakeven = 0

        gross_profit = 0.0
        gross_loss = 0.0

        win_list = []
        loss_list = []

        for t in self.trades:
            pnl = t.get("pnl", 0.0)

            try:
                pnl = float(pnl)
            except Exception:
                pnl = 0.0

            if pnl > 0:
                wins += 1
                gross_profit += pnl
                win_list.append(pnl)
            elif pnl < 0:
                losses += 1
                gross_loss += abs(pnl)
                loss_list.append(pnl)
            else:
                breakeven += 1

        win_rate = (wins / total * 100.0) if total > 0 else 0.0
        net_profit = self.final_value - self.initial_balance

        avg_win = sum(win_list) / len(win_list) if win_list else 0.0
        avg_loss = sum(loss_list) / len(loss_list) if loss_list else 0.0

        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0.0
        expectancy = ((gross_profit - gross_loss) / total) if total > 0 else 0.0

        return {
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "breakeven": breakeven,
            "win_rate_pct": round(win_rate, 2),
            "net_profit": round(net_profit, 2),
            "final_value": round(self.final_value, 2),
            "gross_profit": round(gross_profit, 2),
            "gross_loss": round(gross_loss, 2),
            "avg_win": round(avg_win, 4),
            "avg_loss": round(avg_loss, 4),
            "profit_factor": round(profit_factor, 4),
            "expectancy": round(expectancy, 4)
        }
