# bot_ai/metrics.py
# Расчёт метрик стратегии на основе equity-кривой

import numpy as np

def calculate_metrics(summary_df, initial_balance=1000):
    if summary_df is None or summary_df.empty:
        return {}

    trades = summary_df["signal"].isin(["BUY", "SELL"]).sum()
    final_balance = summary_df["equity"].iloc[-1] if "equity" in summary_df.columns else initial_balance

    returns = summary_df["equity"].pct_change().dropna()
    win_trades = (returns > 0).sum()
    loss_trades = (returns < 0).sum()

    win_rate = round(100 * win_trades / trades, 2) if trades > 0 else 0
    max_drawdown = 0
    if "equity" in summary_df.columns:
        peak = summary_df["equity"].cummax()
        drawdown = (summary_df["equity"] - peak) / peak
        max_drawdown = round(drawdown.min() * 100, 2)

    sharpe = round((returns.mean() / returns.std()) * np.sqrt(252), 2) if not returns.empty and returns.std() != 0 else 0
    profit_factor = round(returns[returns > 0].sum() / abs(returns[returns < 0].sum()), 2) if loss_trades > 0 else float("inf")

    return {
        "trades": trades,
        "win_rate": win_rate,
        "final_balance": round(final_balance, 2),
        "max_drawdown": max_drawdown,
        "sharpe": sharpe,
        "profit_factor": profit_factor
    }
