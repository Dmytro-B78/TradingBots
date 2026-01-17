# metrics.py
# 📊 Расчёт метрик по результатам стратегии

import numpy as np
import pandas as pd

def calculate_metrics(df, initial_balance=10000, fee=0.001):
    df = df.copy()
    df["returns"] = 0.0
    df["position_shifted"] = df["position"].shift(1).fillna(0)

    # 💸 Доходность по сделкам
    df["returns"] = df["position_shifted"] * df["close"].pct_change()
    df["returns"] -= abs(df["position_shifted"].diff().fillna(0)) * fee

    # 📈 Капитал
    df["equity"] = (1 + df["returns"]).cumprod() * initial_balance

    # 📉 Просадка
    df["peak"] = df["equity"].cummax()
    df["drawdown"] = df["equity"] / df["peak"] - 1

    # 🧮 Метрики
    trades = df["signal"].abs().sum()
    win_trades = df[df["returns"] > 0]["returns"].count()
    loss_trades = df[df["returns"] < 0]["returns"].count()
    winrate = 100 * win_trades / (win_trades + loss_trades) if (win_trades + loss_trades) > 0 else 0

    final_balance = df["equity"].iloc[-1]
    max_drawdown = df["drawdown"].min() * 100

    # 📊 Sharpe Ratio
    daily_returns = df["returns"].resample("1D").sum()
    sharpe = (daily_returns.mean() / daily_returns.std()) * np.sqrt(365) if daily_returns.std() != 0 else 0

    # ⚖️ Profit Factor
    gross_profit = df[df["returns"] > 0]["returns"].sum()
    gross_loss = abs(df[df["returns"] < 0]["returns"].sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf

    return {
        "trades": int(trades),
        "winrate": round(winrate, 2),
        "final_balance": round(final_balance, 2),
        "drawdown": round(max_drawdown, 2),
        "sharpe": round(sharpe, 2),
        "profit_factor": round(profit_factor, 2)
    }
