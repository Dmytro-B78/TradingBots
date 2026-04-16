import csv
from bot_ai.strategy.meta_strategy import MetaStrategy

csv_path = "C:\\TradingBots\\candles\\compiled\\SOLUSDT-1h.csv"

def load_csv(path):
    rows = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "timestamp": int(r.get("timestamp") or 0),
                "open": float(r.get("open") or 0),
                "high": float(r.get("high") or 0),
                "low": float(r.get("low") or 0),
                "close": float(r.get("close") or 0),
                "volume": float(r.get("volume") or 0),
            })
    return rows

candles = load_csv(csv_path)
strategy = MetaStrategy()

conf_vals = []
ts_vals = []
slope_vals = []
mom_vals = []

for c in candles:
    state = strategy.compute_meta_state(c)
    conf_vals.append(state["confidence"])
    ts_vals.append(strategy.trend_strength)
    slope_vals.append(strategy.slope)
    mom_vals.append(strategy.momentum)

def stats(name, arr):
    arr = [x for x in arr if x is not None]
    if not arr:
        print(name, ": no data")
        return
    print(name, "min:", min(arr), "max:", max(arr), "avg:", sum(arr)/len(arr))

stats("confidence", conf_vals)
stats("trend_strength", ts_vals)
stats("slope", slope_vals)
stats("momentum", mom_vals)
