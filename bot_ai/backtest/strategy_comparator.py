# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/backtest/strategy_comparator.py
# Назначение: Сравнение стратегий + экспорт + визуализация + логирование
# ============================================

import pandas as pd
import os
import logging
import matplotlib.pyplot as plt
from bot_ai.strategy.breakout import BreakoutStrategy
from bot_ai.strategy.mean_reversion import MeanReversionStrategy
from bot_ai.metrics import calculate_metrics

# === Настройка логирования ===
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/compare.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

STRATEGY_MAP = {
    "breakout": BreakoutStrategy,
    "mean_reversion": MeanReversionStrategy
}

def load_data(symbol, timeframe):
    path = f"data/{symbol}_{timeframe}.csv"
    df = pd.read_csv(path)
    df["time"] = pd.to_datetime(df["time"])
    return df

def run_strategy(strategy_name, df, symbol, params, balance):
    strategy_cls = STRATEGY_MAP.get(strategy_name)
    if not strategy_cls:
        raise ValueError(f"Неизвестная стратегия: {strategy_name}")
    strategy = strategy_cls({"params": params})
    df = strategy.calculate_indicators(df)
    df = strategy.generate_signals(df)
    strategy.backtest(df, initial_balance=balance)
    summary = strategy.summary(symbol)
    metrics = calculate_metrics(summary, initial_balance=balance)
    return metrics

def save_results(df):
    os.makedirs("results", exist_ok=True)
    df.to_csv("results/compare_summary.csv", index=False)
    logging.info("📁 Сохранён: results/compare_summary.csv")

def plot_results(df):
    try:
        plt.figure(figsize=(10, 6))
        df["label"] = df["symbol"] + " | " + df["strategy"]
        bars = plt.bar(df["label"], df["final_balance"], color="skyblue")
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Final Balance ($)")
        plt.title("📈 Сравнение стратегий по доходности")
        plt.tight_layout()
        plt.grid(axis="y", linestyle="--", alpha=0.5)

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, f"{yval:.0f}", va='bottom', ha='center', fontsize=8)

        plt.savefig("results/compare_plot.png")
        logging.info("🖼️ Сохранён график: results/compare_plot.png")
    except Exception as e:
        logging.warning(f"[PLOT] Ошибка при построении графика: {e}")

def compare_strategies(pairs, strategies, timeframe="1h", rsi_threshold=65, capital=10000, risk_pct=1.0, strategy_params=None):
    logging.info("=== Сравнение стратегий начато ===")
    all_results = []

    for symbol in pairs:
        try:
            df = load_data(symbol, timeframe)
            logging.info(f"[DATA] Загружены данные для {symbol}")
        except Exception as e:
            logging.warning(f"[FAIL] {symbol} — ошибка загрузки: {e}")
            continue

        for strat in strategies:
            params = (strategy_params or {}).get(strat, {})
            try:
                metrics = run_strategy(strat, df.copy(), symbol, params, capital)
                row = {"symbol": symbol, "strategy": strat}
                row.update(metrics)
                all_results.append(row)
                logging.info(f"[OK] {symbol} | {strat} | Баланс: {metrics['final_balance']:.2f}")
            except Exception as e:
                logging.warning(f"[ERROR] {symbol} | {strat} — {e}")

    if not all_results:
        logging.error("Нет результатов для сравнения.")
        print("❌ Нет результатов для сравнения.")
        return

    df_results = pd.DataFrame(all_results)
    df_results = df_results.sort_values(by=["symbol", "final_balance"], ascending=[True, False])

    print("\n📊 Сравнение стратегий по всем парам:")
    print(df_results.to_string(index=False))

    save_results(df_results)
    plot_results(df_results)
    logging.info("✅ Сравнение завершено")
