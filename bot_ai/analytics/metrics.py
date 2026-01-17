# bot_ai/analytics/metrics.py
# 📊 Метрики стратегии: прибыль, сделки, winrate, средний риск/прибыль

import pandas as pd

def calculate_metrics(trades: pd.DataFrame) -> dict:
    """
    Принимает DataFrame со сделками и возвращает словарь метрик.
    Ожидаемые колонки: pnl, type
    """
    if trades.empty:
        return {
            "total_pnl": 0,
            "num_trades": 0,
            "win_rate": 0,
            "avg_pnl": 0,
            "profit_factor": 0
        }

    total_pnl = trades["pnl"].sum()
    num_trades = len(trades)
    wins = trades[trades["pnl"] > 0]
    losses = trades[trades["pnl"] < 0]

    win_rate = len(wins) / num_trades if num_trades > 0 else 0
    avg_pnl = trades["pnl"].mean()
    profit_factor = wins["pnl"].sum() / abs(losses["pnl"].sum()) if not losses.empty else float("inf")

    return {
        "total_pnl": round(total_pnl, 2),
        "num_trades": num_trades,
        "win_rate": round(win_rate * 100, 2),
        "avg_pnl": round(avg_pnl, 2),
        "profit_factor": round(profit_factor, 2)
    }
