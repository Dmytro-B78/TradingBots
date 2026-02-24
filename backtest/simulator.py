# bot_ai/backtest/simulator.py
# Класс Simulator — базовая симуляция сделок с расчётом PnL, капитала и метрик

import pandas as pd

class Simulator:
    def __init__(self, initial_capital, risk_per_trade, pair, timeframe):
        self.initial_capital = initial_capital
        self.risk_per_trade = risk_per_trade
        self.pair = pair
        self.timeframe = timeframe
        self.trades = []
        self.capital = initial_capital

    def execute_trade(self, time, side, price):
        # Фиксируем сделку
        trade = {
            "time": time,
            "side": side,
            "price": price,
            "capital_before": self.capital
        }

        # Простейшая модель: фиксированный PnL
        # Buy → +1%, Sell → -0.5%
        if side == "BUY":
            pnl_pct = 0.01
        elif side == "SELL":
            pnl_pct = -0.005
        else:
            pnl_pct = 0

        risk_amount = self.capital * self.risk_per_trade
        pnl = risk_amount * pnl_pct
        self.capital += pnl

        trade["pnl"] = pnl
        trade["capital_after"] = self.capital
        self.trades.append(trade)

    def get_report(self):
        df = pd.DataFrame(self.trades)
        total_trades = len(df)
        wins = df[df["pnl"] > 0].shape[0]
        losses = df[df["pnl"] < 0].shape[0]
        winrate = wins / total_trades if total_trades > 0 else 0
        total_pnl = df["pnl"].sum() if total_trades > 0 else 0
        max_drawdown = self._calculate_drawdown(df["capital_after"]) if total_trades > 0 else 0

        return {
            "total_trades": total_trades,
            "winning_trades": wins,
            "losing_trades": losses,
            "winrate": round(winrate * 100, 2),
            "average_pnl": round(df["pnl"].mean(), 4) if total_trades > 0 else 0,
            "total_return": round((self.capital - self.initial_capital) / self.initial_capital * 100, 2),
            "max_drawdown": round(max_drawdown, 2),
            "profit_factor": round(df[df["pnl"] > 0]["pnl"].sum() / abs(df[df["pnl"] < 0]["pnl"].sum()), 2) if losses > 0 else float("inf"),
            "sharpe_ratio": round(self._calculate_sharpe(df["pnl"]), 2) if total_trades > 1 else 0,
            "final_capital": round(self.capital, 2)
        }

    def _calculate_drawdown(self, equity_curve):
        peak = equity_curve.expanding(min_periods=1).max()
        drawdown = (equity_curve - peak) / peak
        return drawdown.min() * 100  # в процентах

    def _calculate_sharpe(self, pnl_series):
        if pnl_series.std() == 0:
            return 0
        return (pnl_series.mean() / pnl_series.std()) * (len(pnl_series) ** 0.5)
