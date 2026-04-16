import json
import os
from collections import defaultdict

LOG_PATH = "logs/offline_log.txt"

def load_trades():
    trades = []
    with open(LOG_PATH, "r") as f:
        for line in f:
            if "\"kind\": \"trade\"" in line:
                try:
                    trades.append(json.loads(line))
                except:
                    pass
    return trades

def bucket(value, step):
    return int(value // step)

def analyze():
    trades = load_trades()
    if not trades:
        print("No trades found")
        return

    # PnL by duration_bars
    dur_buckets = defaultdict(list)
    for t in trades:
        d = t.get("duration_bars")
        p = t.get("pnl_pct")
        if d is not None and p is not None:
            dur_buckets[bucket(d, 5)].append(p)

    print("=== PnL by duration_bars (bucket=5 bars) ===")
    for b in sorted(dur_buckets.keys()):
        arr = dur_buckets[b]
        avg = sum(arr) / len(arr)
        print(f"{b*5:03d}-{(b+1)*5:03d} bars: avg pnl {avg:.4f} n={len(arr)}")

    # PnL by ATR
    atr_buckets = defaultdict(list)
    for t in trades:
        atr = t.get("atr_1h_entry")
        p = t.get("pnl_pct")
        if atr is not None and p is not None:
            atr_buckets[bucket(atr, 0.5)].append(p)

    print("\n=== PnL by ATR_1h_entry (bucket=0.5) ===")
    for b in sorted(atr_buckets.keys()):
        arr = atr_buckets[b]
        avg = sum(arr) / len(arr)
        print(f"{b*0.5:.1f}-{(b+1)*0.5:.1f} ATR: avg pnl {avg:.4f} n={len(arr)}")

    # PnL by regime
    reg_buckets = defaultdict(list)
    for t in trades:
        r = t.get("local_regime_entry")
        p = t.get("pnl_pct")
        if r and p is not None:
            reg_buckets[r].append(p)

    print("\n=== PnL by local_regime_entry ===")
    for r, arr in reg_buckets.items():
        avg = sum(arr) / len(arr)
        print(f"{r}: avg pnl {avg:.4f} n={len(arr)}")

    # PnL by confidence
    conf_buckets = defaultdict(list)
    for t in trades:
        c = t.get("confidence_entry")
        p = t.get("pnl_pct")
        if c is not None and p is not None:
            conf_buckets[bucket(c, 0.05)].append(p)

    print("\n=== PnL by confidence_entry (bucket=0.05) ===")
    for b in sorted(conf_buckets.keys()):
        arr = conf_buckets[b]
        avg = sum(arr) / len(arr)
        print(f"{b*0.05:.2f}-{(b+1)*0.05:.2f}: avg pnl {avg:.4f} n={len(arr)}")

if __name__ == "__main__":
    analyze()
