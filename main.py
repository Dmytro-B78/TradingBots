# -*- coding: utf-8 -*-
# ============================================
# File: main.py
# Назначение: Запуск стратегий в режиме backtest / live
# ============================================

import argparse
import json
import os
import pandas as pd
from bot_ai.strategy.breakout import BreakoutStrategy
from bot_ai.strategy.mean_reversion import MeanReversionStrategy
from bot_ai.metrics import calculate_metrics

# === Загрузка конфигурации ===
def load_config(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

# === Симуляция торговли ===
def simulate_trading(df, strategy, symbol, balance=1000):
    df = strategy.calculate_indicators(df)
    df = strategy.generate_signals(df)
    strategy.backtest(df, initial_balance=balance)
    summary = strategy.summary(symbol)

    print(f"\n✅ Сигналов BUY/SELL: {df['signal'].isin(['BUY','SELL']).sum()}")

    print("\n📒 Примеры сделок:")
    for t in strategy.trades[-5:]:
        print(f"{t['time']} | {t['signal']:>4} @ {t['price']:.4f} | Баланс: {t['balance']}")

    return summary

# === Анализ результатов ===
def analyze_performance(summary_df, initial_balance):
    metrics = calculate_metrics(summary_df, initial_balance=initial_balance)
    print("\n📊 Метрики стратегии:")
    for k, v in metrics.items():
        print(f"{k:>15}: {v}")
    return metrics

# === Основной запуск ===
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["backtest", "live"], required=True)
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--strategy", required=True)
    parser.add_argument("--timeframe", default="1h")
    parser.add_argument("--balance", type=float, default=1000)
    parser.add_argument("--config", default="config.json")
    args = parser.parse_args()

    print(f"🚀 Запуск в режиме {args.mode} | Пара: {args.symbol} | Таймфрейм: {args.timeframe} | Стратегия: {args.strategy}")

    config = load_config(args.config)
    params = config.get("params", {})

    # Загрузка данных
    df_path = f"data/{args.symbol}_{args.timeframe}.csv"
    if not os.path.exists(df_path):
        print(f"❌ Нет данных: {df_path}")
        return
    df = pd.read_csv(df_path)
    df["time"] = pd.to_datetime(df["time"])

    # Выбор стратегии
    if args.strategy == "breakout":
        strategy = BreakoutStrategy({"params": params})
    elif args.strategy == "mean_reversion":
        strategy = MeanReversionStrategy(params)
    else:
        print(f"❌ Неизвестная стратегия: {args.strategy}")
        return

    # Запуск симуляции
    summary_df = simulate_trading(df, strategy, args.symbol, balance=args.balance)
    if summary_df.empty:
        print("❌ Сделки не найдены.")
        return

    # Анализ
    analyze_performance(summary_df, initial_balance=args.balance)

if __name__ == "__main__":
    main()
