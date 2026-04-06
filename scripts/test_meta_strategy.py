import sys, csv
sys.path.append("C:/TradingBots/NT")

from bot_ai.strategy.meta_strategy import MetaStrategy

path = "C:/TradingBots/candles/compiled/SOLUSDT-1m.csv"
print("Using:", path)

candles = []
with open(path, "r") as f:
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

print("Loaded candles:", len(candles))
print("====================================")

ms = MetaStrategy({})

for c in candles[:-200]:
    ms.on_candle(c)

for i, c in enumerate(candles[-200:]):
    decision = ms.on_candle(c)

    print("------------------------------------")
    print("Index:", i)
    print("Price:", c["close"])
    print("Regime:", ms.regime)

    signals = []
    for strat in ms.strategies:
        s = strat.on_candle(c)
        signals.append((strat.__class__.__name__, s))

    print("Signals:")
    for name, sig in signals:
        print(" ", name, "=>", sig)

    print("Decision:", (decision or {}).get("signal"))
