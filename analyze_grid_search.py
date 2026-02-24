# analyze_grid_search.py
# СЂСџВ§В  Р С’Р Р…Р В°Р В»Р С‘Р В· grid_search.csv Р С‘ Р С–Р ВµР Р…Р ВµРЎР‚Р В°РЎвЂ Р С‘РЎРЏ portfolio_optimized.json

import pandas as pd
import json
import os

# СЂСџвЂњТђ Р вЂ”Р В°Р С–РЎР‚РЎС“Р В·Р С”Р В° РЎР‚Р ВµР В·РЎС“Р В»РЎРЉРЎвЂљР В°РЎвЂљР С•Р Р†
df = pd.read_csv("results/grid_search.csv")

# СЂСџВ§В  Р РЋР С•РЎР‚РЎвЂљР С‘РЎР‚Р С•Р Р†Р С”Р В° Р С—Р С• profit_factor
df = df.sort_values("profit_factor", ascending=False)

# СЂСџР‹Р‡ Р СћР С•Р С—-5 Р С”Р С•Р Р…РЎвЂћР С‘Р С–РЎС“РЎР‚Р В°РЎвЂ Р С‘Р в„–
top = df.head(5)

# СЂСџвЂњВ¦ Р В¤Р С•РЎР‚Р СР С‘РЎР‚РЎС“Р ВµР С Р С—Р С•РЎР‚РЎвЂљРЎвЂћР ВµР В»РЎРЉ
portfolio = []
for _, row in top.iterrows():
    params = {k: row[k] for k in row.index if k not in ["strategy", "pair", "winrate", "drawdown", "sharpe", "profit_factor", "final_balance"]}
    portfolio.append({
        "strategy": row["strategy"],
        "pair": row["pair"],
        "params": params
    })

# СЂСџвЂ™С• Р РЋР С•РЎвЂ¦РЎР‚Р В°Р Р…РЎРЏР ВµР С
os.makedirs("results", exist_ok=True)
with open("results/portfolio_optimized.json", "w", encoding="utf-8") as f:
    json.dump(portfolio, f, indent=2)

print("РІСљвЂ¦ Р СћР С•Р С—-5 Р С”Р С•Р Р…РЎвЂћР С‘Р С–РЎС“РЎР‚Р В°РЎвЂ Р С‘Р в„– РЎРѓР С•РЎвЂ¦РЎР‚Р В°Р Р…Р ВµР Р…РЎвЂ№ Р Р†: results/portfolio_optimized.json")

