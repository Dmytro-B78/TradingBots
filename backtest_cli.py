# ============================================
# ✅ backtest_cli.py — CLI для бэктеста RSI
# Обновление:
# - Поддержка вывода PnL, win_rate, num_trades
# - Поддержка DataFrame-результатов
# - Безопасная обработка None
# Расположение: C:\TradingBots\NT\backtest_cli.py
# ============================================

import argparse
import json
from bot_ai.backtest.backtest_engine import run_backtest
from strategies.rsi import RSIStrategy

parser = argparse.ArgumentParser(description="Бэктест стратегии RSI")
parser.add_argument("--symbol", type=str, required=True, help="Торговый символ (например BTCUSDT)")
parser.add_argument("--profile", type=str, required=True, help="Путь к JSON-профилю")
parser.add_argument("--days", type=int, default=30, help="Глубина истории в днях")
parser.add_argument("--timeframe", type=str, default="1h", help="Таймфрейм (например 1h, 4h)")
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

print("=== 📈 Результаты бэктеста ===")
for symbol, tf_results in results.items():
    for tf, res in tf_results.items():
        print(f"\nСимвол: {symbol} | Таймфрейм: {tf}")
        if res is None:
            print("⚠️ Нет результатов (strategy.run_backtest() вернул None)")
        elif isinstance(res, dict):
            print(f"📊 PnL: {res.get('pnl')}")
            print(f"✅ Win Rate: {res.get('win_rate')}")
            print(f"📌 Trades: {res.get('num_trades')}")
        elif hasattr(res, "tail"):
            print(res.tail(5))
        else:
            print("⚠️ Неизвестный формат результата:", type(res))
