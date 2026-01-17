# -*- coding: utf-8 -*-
# ============================================
# File: backtest/walk_forward.py
# Назначение: Walk-forward анализ стратегии с метриками и HTML-отчётом
# ============================================

import os
import pandas as pd
from backtest.metrics import calculate_metrics
from backtest.report import print_metrics, save_trades_to_csv
from backtest.html_report import generate_html_report
from backtest.equity_plot import plot_equity_curve
from bot_ai.strategy.strategy_selector import select_strategy

def walk_forward_test(df: pd.DataFrame, strategy_name: str, config: dict, window_size: int = 100, step_size: int = 20):
    """
    Пошаговый walk-forward анализ стратегии на данных df
    """
    print(f"[WF] ▶ стратегия={strategy_name} | окно={window_size} | шаг={step_size}")

    strategy = select_strategy(strategy_name)
    if strategy is None:
        print(f"[WF] ❌ Стратегия '{strategy_name}' не найдена")
        return

    all_trades = []
    i = 0
    while i + window_size < len(df):
        window_df = df.iloc[i:i+window_size].copy()
        trades = strategy(config["symbol"], window_df, config)
        all_trades.extend(trades)
        i += step_size

    print(f"[WF] ✅ Всего сигналов: {len(all_trades)}")

    metrics = calculate_metrics(all_trades)
    print_metrics(metrics)

    output_dir = config.get("output_dir", ".")
    os.makedirs(output_dir, exist_ok=True)

    csv_path = os.path.join(output_dir, "backtest_results.csv")
    html_path = os.path.join(output_dir, "backtest_report.html")
    equity_path = os.path.join(output_dir, "equity_curve.png")

    save_trades_to_csv(all_trades, path=csv_path)
    plot_equity_curve(all_trades, filename=equity_path)
    generate_html_report(all_trades, metrics, filename=html_path)
