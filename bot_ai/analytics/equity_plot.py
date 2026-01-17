# -*- coding: utf-8 -*-
# === bot_ai/analytics/equity_plot.py ===
# Equity curve + метрики + гистограмма прибыли/убытков

import os

import matplotlib.pyplot as plt
import pandas as pd

def calculate_metrics(df, initial_balance=1000):
    df = df.copy()
    df = df.sort_values("closed_at")

    # Баланс
    balance = [initial_balance]
    for pnl in df["pnl_usdt"]:
        balance.append(balance[-1] + pnl)
    df["balance"] = balance[1:]

    # Winrate
    wins = df[df["pnl_usdt"] > 0]
    losses = df[df["pnl_usdt"] < 0]
    winrate = len(wins) / len(df) * 100 if len(df) > 0 else 0

    # Средняя прибыль/убыток
    avg_win = wins["pnl_usdt"].mean() if not wins.empty else 0
    avg_loss = losses["pnl_usdt"].mean() if not losses.empty else 0

    # Средний RR
    rr = abs(avg_win / avg_loss) if avg_loss != 0 else float("inf")

    # Максимальная просадка
    peak = df["balance"].cummax()
    drawdown = (df["balance"] - peak) / peak
    max_dd = drawdown.min() * 100

    return df, {
        "Winrate (%)": round(winrate, 2),
        "Avg Win (USDT)": round(avg_win, 2),
        "Avg Loss (USDT)": round(avg_loss, 2),
        "Avg RR": round(rr, 2),
        "Max Drawdown (%)": round(max_dd, 2)
    }

def plot_equity_curve(csv_path="trades_log.csv", initial_balance=1000):
    if not os.path.exists(csv_path):
        print(f"Файл {csv_path} не найден.")
        return

    try:
        df = pd.read_csv(csv_path, parse_dates=["closed_at"])
    except pd.errors.EmptyDataError:
        print("Файл trades_log.csv существует, но он пустой.")
        return

    if df.empty:
        print("Файл trades_log.csv не содержит данных.")
        return

    df, metrics = calculate_metrics(df, initial_balance)

    # === Построение графиков ===
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(
        12, 8), gridspec_kw={"height_ratios": [2, 1]})

    # Equity curve
    ax1.plot(
        df["closed_at"],
        df["balance"],
        label="Equity Curve",
        color="blue",
        linewidth=2)
    ax1.set_title("Equity Curve")
    ax1.set_xlabel("Дата закрытия сделки")
    ax1.set_ylabel("Баланс (USDT)")
    ax1.grid(True)
    ax1.legend()

    # Метрики
    text = "\n".join([f"{k}: {v}" for k, v in metrics.items()])
    fig.text(
        0.75,
        0.4,
        text,
        fontsize=10,
        bbox=dict(
            facecolor="white",
            alpha=0.8))

    # Гистограмма прибыли/убытков
    ax2.hist(df["pnl_usdt"], bins=20, color="green", edgecolor="black")
    ax2.set_title("Распределение прибыли/убытков")
    ax2.set_xlabel("PnL (USDT)")
    ax2.set_ylabel("Количество сделок")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_equity_curve()

