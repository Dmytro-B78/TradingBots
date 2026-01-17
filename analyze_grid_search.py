# analyze_grid_search.py
# 🧠 Анализ grid_search.csv и генерация portfolio_optimized.json

import pandas as pd
import json
import os

# 📥 Загрузка результатов
df = pd.read_csv("results/grid_search.csv")

# 🧠 Сортировка по profit_factor
df = df.sort_values("profit_factor", ascending=False)

# 🎯 Топ-5 конфигураций
top = df.head(5)

# 📦 Формируем портфель
portfolio = []
for _, row in top.iterrows():
    params = {k: row[k] for k in row.index if k not in ["strategy", "pair", "winrate", "drawdown", "sharpe", "profit_factor", "final_balance"]}
    portfolio.append({
        "strategy": row["strategy"],
        "pair": row["pair"],
        "params": params
    })

# 💾 Сохраняем
os.makedirs("results", exist_ok=True)
with open("results/portfolio_optimized.json", "w", encoding="utf-8") as f:
    json.dump(portfolio, f, indent=2)

print("✅ Топ-5 конфигураций сохранены в: results/portfolio_optimized.json")
