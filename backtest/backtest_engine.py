# -*- coding: utf-8 -*-
# ============================================
# File: backtest/backtest_engine.py
# Назначение: Запуск бэктеста с метриками, графиком и HTML-отчётом
# ============================================

import os
from backtest.split import train_test_split
from backtest.metrics import calculate_metrics
from backtest.report import print_metrics, save_trades_to_csv
from backtest.html_report import generate_html_report
from backtest.equity_plot import plot_equity_curve
from bot_ai.strategy.strategy_selector import select_strategy
from bot_ai.utils.data import fetch_ohlcv

def run_backtest(pair: str, strategy_name: str, timeframe: str, config: dict):
    """
    Запускает бэктест стратегии на указанной паре и таймфрейме.
    Делит данные на train/test, применяет стратегию к тестовой выборке,
    рассчитывает метрики, сохраняет график и HTML-отчёт.
    """
    print(f"[BACKTEST] ▶ {pair} | стратегия={strategy_name} | таймфрейм={timeframe}")

    df = fetch_ohlcv(pair, timeframe)
    if df is None or df.empty:
        print("[BACKTEST] ❌ Нет данных")
        return

    # === Train/Test split ===
    train_df, test_df = train_test_split(df, test_size=0.2)
    print(f"[BACKTEST] 📊 Train: {len(train_df)} | Test: {len(test_df)}")

    # === Выбор стратегии ===
    strategy = select_strategy(strategy_name)
    if strategy is None:
        print(f"[BACKTEST] ❌ Стратегия '{strategy_name}' не найдена")
        return

    # === Применение стратегии к тестовой выборке ===
    results = strategy(pair, test_df, config)
    print(f"[BACKTEST] ✅ Сигналов: {len(results)}")

    # === Метрики и отчёты ===
    metrics = calculate_metrics(results)
    print_metrics(metrics)

    output_dir = config.get("output_dir", ".")
    os.makedirs(output_dir, exist_ok=True)

    csv_path = os.path.join(output_dir, "backtest_results.csv")
    html_path = os.path.join(output_dir, "backtest_report.html")
    equity_path = os.path.join(output_dir, "equity_curve.png")

    save_trades_to_csv(results, path=csv_path)
    plot_equity_curve(results, filename=equity_path)
    generate_html_report(results, metrics, filename=html_path)

# === Пример запуска ===
if __name__ == "__main__":
    config = {
        "strategy": "adaptive",
        "symbol": "BTCUSDT",
        "timeframe": "1h",
        "output_dir": "reports"
    }
    run_backtest(config["symbol"], config["strategy"], config["timeframe"], config)
