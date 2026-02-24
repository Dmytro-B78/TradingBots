# СЂСџвЂњРѓ debug_walk.py РІР‚вЂќ Р С•РЎвЂљР В»Р В°Р Т‘Р С”Р В° РЎРѓР С‘Р С–Р Р…Р В°Р В»Р С•Р Р† РЎРѓРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘Р С‘

import os
import json
import pandas as pd
from bot_ai.strategy.strategy_selector import strategy_selector
from bot_ai.utils.data import fetch_ohlcv

def debug_signals(cfg):
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
    if signals.empty:
        print("РІС™В РїС‘РЏ  predict() Р Р†Р ВµРЎР‚Р Р…РЎС“Р В» Р С—РЎС“РЎРѓРЎвЂљР С•Р в„– DataFrame.")
        return

    print(signals.tail(20))  # Р С—Р С•РЎРѓР В»Р ВµР Т‘Р Р…Р С‘Р Вµ 20 РЎРѓРЎвЂљРЎР‚Р С•Р С”
    os.makedirs("results", exist_ok=True)
    signals.to_csv("results/debug_signals.csv", index=False)
    print("СЂСџвЂ™С• Р РЋР С‘Р С–Р Р…Р В°Р В»РЎвЂ№ РЎРѓР С•РЎвЂ¦РЎР‚Р В°Р Р…Р ВµР Р…РЎвЂ№ Р Р† results/debug_signals.csv")

# СЂСџС™Р‚ Р вЂ”Р В°Р С—РЎС“РЎРѓР С”
if __name__ == "__main__":
    with open("bot_ai/config/trader.json", "r", encoding="utf-8-sig") as f:
        cfg = json.load(f)
    debug_signals(cfg["symbols"][0])

