# bot_ai/backtest/strategy_comparator.py
# Сравнение стратегий по всем парам + экспорт в CSV

from bot_ai.backtest.simulator import simulate
import pandas as pd
import os

def compare_strategies(pairs, strategies, timeframe, rsi_threshold, capital, risk_pct, ema_fast=9, ema_slow=21):
    all_results = []
    os.makedirs("results", exist_ok=True)

    for pair in pairs:
        for strategy in strategies:
            df = simulate(
                pair=pair,
                timeframe=timeframe,
                strategy=strategy,
                rsi_threshold=rsi_threshold,
                capital=capital,
                risk_pct=risk_pct,
                ema_fast=ema_fast,
                ema_slow=ema_slow
            )

            if df is None or df.empty:
                print(f"⚠️ Нет сделок")
                continue

            # Сохраняем сделки в CSV
            trades_path = f"results/{pair}_{strategy}.csv"
            df.to_csv(trades_path, index=False)
            print(f"💾 Сделки сохранены: {trades_path}")

            wins = df[df["result"] == "TP"]
            losses = df[df["result"] == "SL"]

            winrate = round(len(wins) / len(df) * 100, 1) if len(df) > 0 else 0
            drawdown = round(df["balance"].max() - df["balance"].min(), 2)

            print(f"\n📊 Сравнение стратегий:")
            print(f"{'Pair':<8} {'Strategy':<12} {'Trades':<7} {'TP':<3} {'SL':<3} {'Winrate %':<10} {'Final Balance':<15} {'Drawdown $'}")
            print(f"{pair:<8} {strategy:<12} {len(df):<7} {len(wins):<3} {len(losses):<3} {winrate:<10} {df['balance'].iloc[-1]:<15.2f} {drawdown:.2f}")

            all_results.append({
                "pair": pair,
                "strategy": strategy,
                "trades": len(df),
                "tp": len(wins),
                "sl": len(losses),
                "winrate": winrate,
                "final_balance": df["balance"].iloc[-1],
                "drawdown": drawdown
            })

    if all_results:
        summary = pd.DataFrame(all_results)
        summary_path = "results/summary.csv"
        summary.to_csv(summary_path, index=False)
        print(f"\n📋 Итоговая таблица:")
        print(summary.to_string(index=False))
        print(f"\n💾 Сводка сохранена: {summary_path}")
    else:
        print("❌ Нет данных для отображения.")
