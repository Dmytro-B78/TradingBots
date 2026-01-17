# ============================================
# 📈 plot_equity_curve.py — График Equity
# --------------------------------------------
# Функция:
# - Строит график кумулятивной прибыли (equity curve)
# - Поддерживает отображение прибыли по сделкам
# Зависимости: matplotlib, pandas
# ============================================

import pandas as pd
import matplotlib.pyplot as plt

def plot_equity_curve(equity: pd.Series, title: str = "Equity Curve"):
    """
    Строит график equity curve

    Параметры:
    - equity: Series с индексом datetime и значениями equity
    - title: заголовок графика (по умолчанию: Equity Curve)

    Вывод:
    - Линия equity curve
    """
    if equity is None or equity.empty:
        print("[plot] Пустая equity curve — нечего рисовать.")
        return

    plt.figure(figsize=(12, 4))
    equity.plot(color="blue", linewidth=2)
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
