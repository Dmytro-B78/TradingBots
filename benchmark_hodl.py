# === benchmark_hodl.py — сравнение стратегии HODL с остальными ===

import pandas as pd

from bot_ai import data_loader

# === 1. Загрузка исторических данных ===
symbol = "BTCUSDT"
interval = "1h"
csv_path = f"data/{symbol}_{interval}.csv"
df = data_loader.load_csv_data(csv_path)

# === 2. Параметры капитала ===
capital = 10000
entry_price = df["close"].iloc[0]
exit_price = df["close"].iloc[-1]

# === 3. Расчёт доходности HODL ===
return_pct = (exit_price - entry_price) / entry_price
final_value = capital * (1 + return_pct)

metrics = {
    "strategy": "hodl",
    "total_return": round(return_pct, 3),
    "final_value": round(final_value, 3),
    "num_trades": 1,
    "win_rate": 1.0 if return_pct > 0 else 0.0,
    "avg_trade_return": round(return_pct, 3),
    "sharpe_ratio": 0.0,
    "max_drawdown": 0.0,
    "approved_trades": 1
}

# === 4. Вывод результатов ===
print("\n?? HODL-бенчмарк:\n")
for k, v in metrics.items():
    print(f"{k}: {v}")

# === 5. Сохранение в CSV ===
df_result = pd.DataFrame([metrics])
df_result.to_csv("results/hodl_benchmark.csv", index=False)
print("\n? HODL метрики сохранены в: results/hodl_benchmark.csv")

