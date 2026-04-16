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
bias_vals = []
local = {}
global_ = {}

for c in candles[:2000]:
    state = strategy.compute_meta_state(c)
    conf_vals.append(state["confidence"])
    bias_vals.append(state["mtf_bias_4h"])

    local[state["local_regime"]] = local.get(state["local_regime"], 0) + 1
    global_[state["global_regime"]] = global_.get(state["global_regime"], 0) + 1

print("Avg confidence:", sum(conf_vals)/len(conf_vals))
print("Avg mtf_bias_4h:", sum(bias_vals)/len(bias_vals))
print("Local regimes:", local)
print("Global regimes:", global_)
