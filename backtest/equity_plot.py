# -*- coding: utf-8 -*-
# ============================================
# File: backtest/equity_plot.py
# Назначение: Построение и сохранение графика equity curve
# ============================================

import matplotlib.pyplot as plt
import pandas as pd

def plot_equity_curve(trades: list, initial_balance: float = 10000.0, filename: str = "equity_curve.png"):
    """
    Строит и сохраняет график equity curve по списку сделок
    """
    if not trades:
        print("❌ Нет сделок для построения графика")
        return

    balance = initial_balance
    equity = [balance]

    for trade in trades:
        pnl = trade.get("pnl", 0)
        balance += pnl
        equity.append(balance)

    df = pd.DataFrame({"equity": equity})
    df["equity"].plot(figsize=(10, 4), title="Equity Curve", grid=True)
    plt.xlabel("Сделка")
    plt.ylabel("Баланс")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"📈 График сохранён: {filename}")
