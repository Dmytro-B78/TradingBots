# ============================================
# File: analyze_signals.py
# Назначение: Сбор метрик по стратегиям из paper_logs/*.csv
# ============================================

import os
import pandas as pd
import glob

def extract_info(filename):
    base = os.path.basename(filename).replace(".csv", "")
    parts = base.split("_")
    strategy = parts[0]
    pair = parts[1]
    return strategy, pair

if __name__ == "__main__":
    files = glob.glob("paper_logs/*.csv")
    summary = []

    for file in files:
        strategy, pair = extract_info(file)
        df = pd.read_csv(file)
        if df.empty:
            continue

        num_signals = len(df)
        num_trades = df["entry_time"].nunique() if "entry_time" in df.columns else 0
        avg_pnl = df["pnl"].mean() if "pnl" in df.columns else None

        summary.append({
            "strategy": strategy,
            "pair": pair,
            "signals": num_signals,
            "trades": num_trades,
            "avg_pnl": round(avg_pnl, 4) if avg_pnl is not None else None
        })

    if summary:
        df_summary = pd.DataFrame(summary)
        df_summary.sort_values(by=["trades", "avg_pnl"], ascending=[False, False], inplace=True)
        df_summary.to_csv("paper_logs/summary.csv", index=False)
        print("✅ Сводка сохранена в: paper_logs/summary.csv\n")
        print(df_summary.head(20).to_string(index=False))
    else:
        print("⚠️ Нет данных для анализа. Убедись, что в папке paper_logs есть CSV-файлы.")
