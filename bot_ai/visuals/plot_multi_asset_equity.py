# ============================================
# 📊 plot_multi_asset_equity.py — Multi-Equity
# --------------------------------------------
# Функция:
# - Строит график equity curve по нескольким стратегиям/парам
# - Поддерживает сравнение доходностей
# Зависимости: matplotlib, pandas
# ============================================

import pandas as pd
import matplotlib.pyplot as plt

def plot_multi_asset_equity(equity_dict: dict, normalize: bool = True, title: str = "Multi-Asset Equity Curve"):
    """
    Визуализация equity по нескольким стратегиям или активам

    Параметры:
    - equity_dict: словарь {label: pd.Series}, где Series — equity с datetime-индексом
    - normalize: если True — нормализует все кривые к 1.0 в начале
    - title: заголовок графика

    Вывод:
    - Линии equity для каждого ключа
    """
    if not equity_dict:
        print("[plot] Нет данных для отображения.")
        return

    plt.figure(figsize=(14, 5))

    for label, series in equity_dict.items():
        if normalize:
            series = series / series.iloc[0]
        plt.plot(series, label=label)

    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Equity (normalized)" if normalize else "Equity")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
