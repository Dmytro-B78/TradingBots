# ============================================
# РІСљвЂ¦ backtest_cli.py РІР‚вЂќ CLI Р Т‘Р В»РЎРЏ Р В±РЎРЊР С”РЎвЂљР ВµРЎРѓРЎвЂљР В° RSI
# Р С›Р В±Р Р…Р С•Р Р†Р В»Р ВµР Р…Р С‘Р Вµ:
# - Р СџР С•Р Т‘Р Т‘Р ВµРЎР‚Р В¶Р С”Р В° Р Р†РЎвЂ№Р Р†Р С•Р Т‘Р В° PnL, win_rate, num_trades
# - Р СџР С•Р Т‘Р Т‘Р ВµРЎР‚Р В¶Р С”Р В° DataFrame-РЎР‚Р ВµР В·РЎС“Р В»РЎРЉРЎвЂљР В°РЎвЂљР С•Р Р†
# - Р вЂР ВµР В·Р С•Р С—Р В°РЎРѓР Р…Р В°РЎРЏ Р С•Р В±РЎР‚Р В°Р В±Р С•РЎвЂљР С”Р В° None
# Р В Р В°РЎРѓР С—Р С•Р В»Р С•Р В¶Р ВµР Р…Р С‘Р Вµ: C:\TradingBots\NT\backtest_cli.py
# ============================================

import argparse
import json
from bot_ai.backtest.backtest_engine import run_backtest
from strategies.rsi import RSIStrategy

parser = argparse.ArgumentParser(description="Р вЂРЎРЊР С”РЎвЂљР ВµРЎРѓРЎвЂљ РЎРѓРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘Р С‘ RSI")
parser.add_argument("--symbol", type=str, required=True, help="Р СћР С•РЎР‚Р С–Р С•Р Р†РЎвЂ№Р в„– РЎРѓР С‘Р СР Р†Р С•Р В» (Р Р…Р В°Р С—РЎР‚Р С‘Р СР ВµРЎР‚ BTCUSDT)")
parser.add_argument("--profile", type=str, required=True, help="Р СџРЎС“РЎвЂљРЎРЉ Р С” JSON-Р С—РЎР‚Р С•РЎвЂћР С‘Р В»РЎР‹")
parser.add_argument("--days", type=int, default=30, help="Р вЂњР В»РЎС“Р В±Р С‘Р Р…Р В° Р С‘РЎРѓРЎвЂљР С•РЎР‚Р С‘Р С‘ Р Р† Р Т‘Р Р…РЎРЏРЎвЂ¦")
parser.add_argument("--timeframe", type=str, default="1h", help="Р СћР В°Р в„–Р СРЎвЂћРЎР‚Р ВµР в„–Р С (Р Р…Р В°Р С—РЎР‚Р С‘Р СР ВµРЎР‚ 1h, 4h)")
args = parser.parse_args()

with open(args.profile, "r", encoding="utf-8") as f:
    config = json.load(f)

rsi_cfg = config.get("rsi_reversal", {})

results = run_backtest(
    cfg=rsi_cfg,
    pairs=[args.symbol],
    strategy_fn=RSIStrategy,
    strategy_name="rsi_reversal",
    days=args.days,
    timeframes=[args.timeframe]
)

print("=== СЂСџвЂњв‚¬ Р В Р ВµР В·РЎС“Р В»РЎРЉРЎвЂљР В°РЎвЂљРЎвЂ№ Р В±РЎРЊР С”РЎвЂљР ВµРЎРѓРЎвЂљР В° ===")
for symbol, tf_results in results.items():
    for tf, res in tf_results.items():
        print(f"\nР РЋР С‘Р СР Р†Р С•Р В»: {symbol} | Р СћР В°Р в„–Р СРЎвЂћРЎР‚Р ВµР в„–Р С: {tf}")
        if res is None:
            print("РІС™В РїС‘РЏ Р СњР ВµРЎвЂљ РЎР‚Р ВµР В·РЎС“Р В»РЎРЉРЎвЂљР В°РЎвЂљР С•Р Р† (strategy.run_backtest() Р Р†Р ВµРЎР‚Р Р…РЎС“Р В» None)")
        elif isinstance(res, dict):
            print(f"СЂСџвЂњР‰ PnL: {res.get('pnl')}")
            print(f"РІСљвЂ¦ Win Rate: {res.get('win_rate')}")
            print(f"СЂСџвЂњРЉ Trades: {res.get('num_trades')}")
        elif hasattr(res, "tail"):
            print(res.tail(5))
        else:
            print("РІС™В РїС‘РЏ Р СњР ВµР С‘Р В·Р Р†Р ВµРЎРѓРЎвЂљР Р…РЎвЂ№Р в„– РЎвЂћР С•РЎР‚Р СР В°РЎвЂљ РЎР‚Р ВµР В·РЎС“Р В»РЎРЉРЎвЂљР В°РЎвЂљР В°:", type(res))

