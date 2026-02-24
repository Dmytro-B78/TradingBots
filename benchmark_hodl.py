# === benchmark_hodl.py РІР‚вЂќ РЎРѓРЎР‚Р В°Р Р†Р Р…Р ВµР Р…Р С‘Р Вµ РЎРѓРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘Р С‘ HODL РЎРѓ Р С•РЎРѓРЎвЂљР В°Р В»РЎРЉР Р…РЎвЂ№Р СР С‘ ===

import pandas as pd

from bot_ai import data_loader

# === 1. Р вЂ”Р В°Р С–РЎР‚РЎС“Р В·Р С”Р В° Р С‘РЎРѓРЎвЂљР С•РЎР‚Р С‘РЎвЂЎР ВµРЎРѓР С”Р С‘РЎвЂ¦ Р Т‘Р В°Р Р…Р Р…РЎвЂ№РЎвЂ¦ ===
symbol = "BTCUSDT"
interval = "1h"
csv_path = f"data/{symbol}_{interval}.csv"
df = data_loader.load_csv_data(csv_path)

# === 2. Р СџР В°РЎР‚Р В°Р СР ВµРЎвЂљРЎР‚РЎвЂ№ Р С”Р В°Р С—Р С‘РЎвЂљР В°Р В»Р В° ===
capital = 10000
entry_price = df["close"].iloc[0]
exit_price = df["close"].iloc[-1]

# === 3. Р В Р В°РЎРѓРЎвЂЎРЎвЂРЎвЂљ Р Т‘Р С•РЎвЂ¦Р С•Р Т‘Р Р…Р С•РЎРѓРЎвЂљР С‘ HODL ===
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

# === 4. Р вЂ™РЎвЂ№Р Р†Р С•Р Т‘ РЎР‚Р ВµР В·РЎС“Р В»РЎРЉРЎвЂљР В°РЎвЂљР С•Р Р† ===
print("\n?? HODL-Р В±Р ВµР Р…РЎвЂЎР СР В°РЎР‚Р С”:\n")
for k, v in metrics.items():
    print(f"{k}: {v}")

# === 5. Р РЋР С•РЎвЂ¦РЎР‚Р В°Р Р…Р ВµР Р…Р С‘Р Вµ Р Р† CSV ===
df_result = pd.DataFrame([metrics])
df_result.to_csv("results/hodl_benchmark.csv", index=False)
print("\n? HODL Р СР ВµРЎвЂљРЎР‚Р С‘Р С”Р С‘ РЎРѓР С•РЎвЂ¦РЎР‚Р В°Р Р…Р ВµР Р…РЎвЂ№ Р Р†: results/hodl_benchmark.csv")


