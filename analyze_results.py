# analyze_results.py
# 📊 Генерирует сводку лучших стратегий
# ✅ Strategy и pair извлекаются из имени файла (например: gridsearch_rsi_macd_PAXGUSDT.csv)

import os
import pandas as pd
import glob

# 🧠 Извлекаем strategy и pair из имени файла
def extract_info(filename):
    base = os.path.basename(filename).replace(".csv", "")
    base = base.replace("gridsearch_", "")
    parts = base.split("_")
    strategy = "_".join(parts[:2])  # например: rsi_macd
    pair = "_".join(parts[2:])      # например: PAXGUSDT
    return strategy, pair

# 📈 Формула оценки стратегии
def score(row):
    return row["final_balance"] + row["winrate"] * 10 - row["drawdown"]

# 🚀 Основной блок
if __name__ == "__main__":
    files = glob.glob("results/gridsearch_*.csv")
    summary = []

    for file in files:
        strategy, pair = extract_info(file)
        df = pd.read_csv(file)
        if df.empty:
            continue
        best = df.iloc[0]
        summary.append({
            "strategy": strategy,
            "pair": pair,
            "trades": best["trades"],
            "winrate": best["winrate"],
            "final_balance": best["final_balance"],
            "drawdown": best["drawdown"],
            "score": score(best)
        })

    if summary:
        df_summary = pd.DataFrame(summary)
        df_summary.sort_values(by="score", ascending=False, inplace=True)
        df_summary.to_csv("results/best_strategies.csv", index=False)
        print("✅ Сводка сохранена: results/best_strategies.csv\n")
        print(df_summary.head(20).to_string(index=False))
    else:
        print("❌ Нет данных для анализа.")
