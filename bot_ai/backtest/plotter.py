# bot_ai/backtest/plotter.py
# Визуализация сигналов и уровней TP/SL на графике

import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_signals(df, signals, pair, strategy):
    if df.empty or not signals:
        print(f"📉 [{pair} | {strategy}] Нет данных для графика")
        return

    os.makedirs("plots", exist_ok=True)

    fig, ax = plt.subplots(2 if strategy == "rsi" else 1, 1, figsize=(12, 6), sharex=True)

    if strategy == "rsi":
        ax_price, ax_rsi = ax
    else:
        ax_price = ax

    # График цены
    ax_price.plot(df["timestamp"], df["close"], label="Close", color="black", linewidth=1)

    # Отметки сигналов и уровней
    for i in range(min(len(signals), len(df))):
        ts = df["timestamp"].iloc[i]
        price = df["close"].iloc[i]
        if "buy" in signals[i]:
            ax_price.scatter(ts, price, marker="o", color="green", label="Buy" if i == 0 else "", zorder=5)
            ax_price.axhline(price * 1.02, color="green", linestyle="--", linewidth=0.8, alpha=0.5)
            ax_price.axhline(price * 0.98, color="red", linestyle="--", linewidth=0.8, alpha=0.5)
        elif "sell" in signals[i]:
            ax_price.scatter(ts, price, marker="o", color="red", label="Sell" if i == 0 else "", zorder=5)
            ax_price.axhline(price * 0.98, color="green", linestyle="--", linewidth=0.8, alpha=0.5)
            ax_price.axhline(price * 1.02, color="red", linestyle="--", linewidth=0.8, alpha=0.5)

    ax_price.set_title(f"{pair} | {strategy}")
    ax_price.set_ylabel("Price")
    ax_price.legend()

    # RSI-график
    if strategy == "rsi" and "rsi" in df.columns:
        ax_rsi.plot(df["timestamp"], df["rsi"], label="RSI", color="blue")
        ax_rsi.axhline(70, color="red", linestyle="--", linewidth=0.8)
        ax_rsi.axhline(30, color="green", linestyle="--", linewidth=0.8)
        ax_rsi.set_ylabel("RSI")
        ax_rsi.set_ylim(0, 100)
        ax_rsi.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()
    path = f"plots/{pair}_{strategy}.png"
    plt.savefig(path)
    plt.close()
    print(f"🖼️ График сохранён: {path}")
