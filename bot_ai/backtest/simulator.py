# ============================================
# File: bot_ai/backtest/simulator.py
# Purpose: Trade simulator with commission and stop-loss support
# Format: UTF-8 without BOM
# ============================================

import pandas as pd
from bot_ai.data_loader import load_data

# === Signal-based strategy simulation ===
def simulate(pair, strategy_class, cfg, timeframe="1h"):
    df = load_data(pair, timeframe)
    strat = strategy_class(df, cfg)
    strat.generate_signals()
    return strat.get_dataframe()

# === Trade execution simulator ===
class Simulator:
    def __init__(self, initial_capital, risk_per_trade, pair, timeframe, commission=0.001, stop_loss_pct=None):
        self.initial_capital = initial_capital
        self.risk_per_trade = risk_per_trade
        self.pair = pair
        self.timeframe = timeframe
        self.commission = commission
        self.stop_loss_pct = stop_loss_pct
        self.trades = []
        self.capital = initial_capital
        self.position_price = None
        self.position_time = None

    def execute_trade(self, time, side, price):
        trade = {
            "time": time,
            "side": side,
            "price": price,
            "capital_before": self.capital,
            "pnl": 0.0,
            "capital_after": self.capital,
            "note": "ignored"
        }

        risk_amount = self.capital * self.risk_per_trade
        pnl = 0

        if side == "BUY":
            self.position_price = price
            self.position_time = time
            trade["note"] = "entry"

        elif side == "SELL" and self.position_price is not None:
            raw_return = (price - self.position_price) / self.position_price
            pnl = risk_amount * raw_return

            if self.stop_loss_pct:
                max_loss = -risk_amount * self.stop_loss_pct
                pnl = max(pnl, max_loss)
                trade["note"] = "exit (SL applied)" if pnl == max_loss else "exit"
            else:
                trade["note"] = "exit"

            total_commission = (self.position_price + price) * self.commission
            pnl -= total_commission

            self.position_price = None
            self.position_time = None

        self.capital += pnl
        trade["pnl"] = pnl
        trade["capital_after"] = self.capital
        self.trades.append(trade)

    def get_report(self):
        if not self.trades:
            return {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "winrate": 0.0,
                "average_pnl": 0.0,
                "total_return": 0.0,
                "max_drawdown": 0.0,
                "profit_factor": 0.0,
                "sharpe_ratio": 0.0,
                "final_capital": self.initial_capital,
                "open_position_price": self.position_price,
                "open_position_time": self.position_time
            }, pd.DataFrame()

        df = pd.DataFrame(self.trades)
        total_trades = len(df)
        wins = df[df["pnl"] > 0].shape[0]
        losses = df[df["pnl"] < 0].shape[0]
        winrate = wins / total_trades if total_trades > 0 else 0
        max_drawdown = self._calculate_drawdown(df["capital_after"]) if total_trades > 0 else 0

        report = {
            "total_trades": total_trades,
            "winning_trades": wins,
            "losing_trades": losses,
            "winrate": round(winrate * 100, 2),
            "average_pnl": round(df["pnl"].mean(), 4),
            "total_return": round((self.capital - self.initial_capital) / self.initial_capital * 100, 2),
            "max_drawdown": round(max_drawdown, 2),
            "profit_factor": round(df[df["pnl"] > 0]["pnl"].sum() / abs(df[df["pnl"] < 0]["pnl"].sum()), 2) if losses > 0 else float("inf"),
            "sharpe_ratio": round(self._calculate_sharpe(df["pnl"]), 2) if total_trades > 1 else 0,
            "final_capital": round(self.capital, 2),
            "open_position_price": self.position_price,
            "open_position_time": self.position_time
        }

        return report, df

    def _calculate_drawdown(self, equity_curve):
        peak = equity_curve.expanding(min_periods=1).max()
        drawdown = (equity_curve - peak) / peak
        return drawdown.min() * 100

    def _calculate_sharpe(self, pnl_series):
        if pnl_series.std() == 0:
            return 0
        return (pnl_series.mean() / pnl_series.std()) * (len(pnl_series) ** 0.5)

    def get_open_position(self):
        if self.position_price is not None:
            return {
                "price": self.position_price,
                "time": self.position_time
            }
        return None
