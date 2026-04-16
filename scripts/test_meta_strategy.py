import csv
from collections import defaultdict
from bot_ai.strategy.meta_strategy import MetaStrategy

CSV_PATH = "C:/TradingBots/candles/compiled/SOLUSDT-1h.csv"


def load_candles(path):
    candles = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 6:
                continue
            candles.append({
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
                "volume": float(row[5])
            })
    return candles


def main():
    print("====================================")
    print(f"Diagnostic test: {CSV_PATH}")
    print("====================================")

    candles = load_candles(CSV_PATH)
    print(f"Loaded candles: {len(candles)}")

    meta = MetaStrategy({})
    position = None

    strategy_counters = defaultdict(lambda: {"BUY": 0, "SELL": 0})

    for i, candle in enumerate(candles):
        decision = meta.on_candle(candle)

        for strat in meta.strategies:
            name = strat.__class__.__name__
            sig = strat.on_candle(candle)
            if sig == "BUY":
                strategy_counters[name]["BUY"] += 1
            elif sig == "SELL":
                strategy_counters[name]["SELL"] += 1

        if decision:
            if decision.get("signal") == "OPEN_LONG":
                position = "LONG"
            elif decision.get("signal") == "CLOSE_LONG":
                position = None

        if i > 0 and i % 5000 == 0:
            print("------------------------------------")
            print(f"Index: {i}")
            print(f"Price: {candle['close']}")
            print(f"Regime: {meta.regime}")
            print(f"Position: {position}")

    print("====================================")
    print("Strategy signal counters")
    print("====================================")

    for name, counts in sorted(strategy_counters.items()):
        print(f"{name:25s} BUY: {counts['BUY']:6d}  SELL: {counts['SELL']:6d}")

    print("====================================")
    print("Done.")


if __name__ == "__main__":
    main()
