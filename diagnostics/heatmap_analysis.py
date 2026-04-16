import json
from collections import defaultdict

LOG_PATH = "logs/offline_log.txt"


def load_trades():
    trades = []
    with open(LOG_PATH, "r") as f:
        for line in f:
            if "\"kind\": \"trade\"" in line:
                try:
                    trades.append(json.loads(line))
                except Exception:
                    pass
    return trades


def bucket(value, step):
    return int(value // step)


def print_heatmap_atr_regime(trades):
    buckets = defaultdict(list)
    for t in trades:
        atr = t.get("atr_1h_entry")
        regime = t.get("local_regime_entry")
        pnl = t.get("pnl_pct")
        if atr is None or regime is None or pnl is None:
            continue
        b = bucket(atr, 0.5)
        buckets[(regime, b)].append(pnl)

    regimes = sorted({k[0] for k in buckets.keys()})
    bmin = min(b for (_, b) in buckets.keys())
    bmax = max(b for (_, b) in buckets.keys())

    print("=== Heatmap: ATR_1h_entry x local_regime_entry (bucket=0.5) ===")
    header = "regime \\ ATR"
    for b in range(bmin, bmax + 1):
        header += f" | {b*0.5:4.1f}-{(b+1)*0.5:4.1f}"
    print(header)
    print("-" * len(header))

    for regime in regimes:
        row = f"{regime:12s}"
        for b in range(bmin, bmax + 1):
            arr = buckets.get((regime, b))
            if arr:
                avg = sum(arr) / len(arr)
                row += f" | {avg:8.2f}"
            else:
                row += " |    ----"
        print(row)
    print()


def print_heatmap_conf_regime(trades):
    buckets = defaultdict(list)
    for t in trades:
        conf = t.get("confidence_entry")
        regime = t.get("local_regime_entry")
        pnl = t.get("pnl_pct")
        if conf is None or regime is None or pnl is None:
            continue
        b = bucket(conf, 0.05)
        buckets[(regime, b)].append(pnl)

    regimes = sorted({k[0] for k in buckets.keys()})
    bmin = min(b for (_, b) in buckets.keys())
    bmax = max(b for (_, b) in buckets.keys())

    print("=== Heatmap: confidence_entry x local_regime_entry (bucket=0.05) ===")
    header = "regime \\ conf"
    for b in range(bmin, bmax + 1):
        header += f" | {b*0.05:4.2f}-{(b+1)*0.05:4.2f}"
    print(header)
    print("-" * len(header))

    for regime in regimes:
        row = f"{regime:12s}"
        for b in range(bmin, bmax + 1):
            arr = buckets.get((regime, b))
            if arr:
                avg = sum(arr) / len(arr)
                row += f" | {avg:8.2f}"
            else:
                row += " |    ----"
        print(row)
    print()


def print_heatmap_duration_pnl(trades):
    buckets = defaultdict(list)
    for t in trades:
        dur = t.get("duration_bars")
        pnl = t.get("pnl_pct")
        if dur is None or pnl is None:
            continue
        b = bucket(dur, 5)
        buckets[b].append(pnl)

    if not buckets:
        print("No duration data")
        return

    bmin = min(buckets.keys())
    bmax = max(buckets.keys())

    print("=== Heatmap: duration_bars x PnL (bucket=5 bars) ===")
    print("bucket_range  | avg_pnl   | count")
    print("----------------------------------")
    for b in range(bmin, bmax + 1):
        arr = buckets.get(b)
        if arr:
            avg = sum(arr) / len(arr)
            print(f"{b*5:03d}-{(b+1)*5:03d} bars | {avg:8.2f} | {len(arr):5d}")
        else:
            print(f"{b*5:03d}-{(b+1)*5:03d} bars |    ----  |     0")
    print()


def main():
    trades = load_trades()
    if not trades:
        print("No trades found")
        return

    print_heatmap_atr_regime(trades)
    print_heatmap_conf_regime(trades)
    print_heatmap_duration_pnl(trades)


if __name__ == "__main__":
    main()
