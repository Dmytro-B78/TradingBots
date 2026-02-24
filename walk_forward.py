# СЂСџвЂњРѓ walk_forward.py РІР‚вЂќ Р С‘РЎРѓРЎвЂљР С•РЎР‚Р С‘РЎвЂЎР ВµРЎРѓР С”Р С‘Р в„– Р С—РЎР‚Р С•Р С–Р С•Р Р… РЎРѓРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘Р С‘

import os
import json
import pandas as pd
from bot_ai.strategy.strategy_selector import strategy_selector
from bot_ai.risk.manager import RiskManager
from bot_ai.utils.data import fetch_ohlcv

def walk_forward(cfg):
    pair = cfg["pair"]
    timeframe = cfg.get("interval", "1h")
    strategy_name = cfg.get("strategy", "volatile")

    StrategyClass = strategy_selector.get(strategy_name)
    if StrategyClass is None:
        print(f"РІСњРЉ Р РЋРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘РЎРЏ '{strategy_name}' Р Р…Р Вµ Р Р…Р В°Р в„–Р Т‘Р ВµР Р…Р В°.")
        return

    strategy = StrategyClass(cfg)
    df = fetch_ohlcv(pair, timeframe=timeframe, limit=1000)
    if df is None or df.empty:
        print("РІСњРЉ Р СњР ВµРЎвЂљ Р Т‘Р В°Р Р…Р Р…РЎвЂ№РЎвЂ¦ Р Т‘Р В»РЎРЏ Р В°Р Р…Р В°Р В»Р С‘Р В·Р В°.")
        return

    signals = strategy.predict(df)
    risk = RiskManager(cfg)
    trades = risk.apply(signals, df)

    if not trades:
        print("РІС™В РїС‘РЏ  Р РЋР Т‘Р ВµР В»Р С”Р С‘ Р Р…Р Вµ Р Р…Р В°Р в„–Р Т‘Р ВµР Р…РЎвЂ№.")
        return

    results = pd.DataFrame(trades)
    results["pnl"] = results.apply(lambda row: calc_pnl(row), axis=1)

    total = results["pnl"].sum()
    wins = results[results["pnl"] > 0].shape[0]
    losses = results[results["pnl"] <= 0].shape[0]
    winrate = 100 * wins / (wins + losses)

    print(f"\nСЂСџвЂњв‚¬ Р В Р ВµР В·РЎС“Р В»РЎРЉРЎвЂљР В°РЎвЂљРЎвЂ№ РЎРѓРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘Р С‘ '{strategy_name}' Р Р…Р В° {pair} [{timeframe}]:")
    print(f"Р вЂ™РЎРѓР ВµР С–Р С• РЎРѓР Т‘Р ВµР В»Р С•Р С”: {len(results)}")
    print(f"Р СџРЎР‚Р С‘Р В±РЎвЂ№Р В»РЎРЉР Р…РЎвЂ№РЎвЂ¦: {wins}, Р Р€Р В±РЎвЂ№РЎвЂљР С•РЎвЂЎР Р…РЎвЂ№РЎвЂ¦: {losses}, Winrate: {winrate:.2f}%")
    print(f"Р РЋРЎС“Р СР СР В°РЎР‚Р Р…РЎвЂ№Р в„– PnL: {total:.2f} USDT")

    os.makedirs("results", exist_ok=True)
    results.to_csv(f"results/walk_forward_results.csv", index=False)
    print("СЂСџвЂ™С• Р РЋР Т‘Р ВµР В»Р С”Р С‘ РЎРѓР С•РЎвЂ¦РЎР‚Р В°Р Р…Р ВµР Р…РЎвЂ№ Р Р† results/walk_forward_results.csv")

def calc_pnl(row):
    if row["direction"] == "long":
        return row["tp"] - row["entry"]
    elif row["direction"] == "short":
        return row["entry"] - row["tp"]
    return 0

# СЂСџС™Р‚ Р вЂ”Р В°Р С—РЎС“РЎРѓР С”
if __name__ == "__main__":
    with open("bot_ai/config/trader.json", "r", encoding="utf-8-sig") as f:
        cfg = json.load(f)
    walk_forward(cfg["symbols"][0])

