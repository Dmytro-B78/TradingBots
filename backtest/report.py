# -*- coding: utf-8 -*-
# ============================================
# File: backtest/report.py
# Назначение: Вывод и сохранение отчёта по стратегии
# ============================================

import pandas as pd

def print_metrics(metrics: dict):
    """
    Печатает метрики стратегии в консоль
    """
    print("\n📈 Результаты стратегии:")
    for key, value in metrics.items():
        print(f"  {key.replace('_', ' ').capitalize()}: {value}")

def save_trades_to_csv(trades: list, path: str = "backtest_results.csv"):
    """
    Сохраняет список сделок в CSV-файл
    """
    if not trades:
        print("❌ Нет сделок для сохранения")
        return

    df = pd.DataFrame(trades)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"💾 Сделки сохранены в: {path}")
