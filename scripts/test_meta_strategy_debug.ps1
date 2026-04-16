# ================================================================
# NT-Tech 2026 - MetaStrategy Diagnostic Tester (Extended)
# File: C:\TradingBots\NT\scripts\test_meta_strategy_debug.ps1
# ASCII-only, deterministic, no Cyrillic
# Description:
#   Diagnostic runner for MetaStrategy 8.4-M with ExtendedMetaLogger.
#   Loads CSV candles, computes meta_state and meta_signal,
#   prints checkpoints with internal debug info from logger.
# ================================================================

param(
    [string]$pair = "SOLUSDT-1h-2026-03.csv"
)

Write-Host "Running MetaStrategy diagnostic test..."
Write-Host "============================================"

$basePath = "C:\TradingBots\candles\compiled"
$csvPath = Join-Path $basePath $pair

if (-not (Test-Path $csvPath)) {
    Write-Host "ERROR: File not found:"
    Write-Host "  $csvPath"
    Write-Host "Available files:"
    Get-ChildItem $basePath
    exit
}

Write-Host "Using file: $csvPath"
Write-Host "File size: $((Get-Item $csvPath).Length) bytes"
Write-Host "===================================="

Set-Content -Path "__meta_debug.py" -Encoding ASCII -Value @"
# ================================================================
# NT-Tech 2026 - MetaStrategy Diagnostic Script (Extended)
# File: __meta_debug.py (auto-generated)
# ASCII-only, deterministic
# ================================================================

import os
import time
import csv
from collections import defaultdict

from bot_ai.strategy.meta.meta_strategy import MetaStrategy

path = r'$csvPath'
fname = os.path.basename(path)

print("====================================")
print("Diagnostic test:", fname)
print("====================================")

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

total = len(candles)
print("Loaded candles:", total)

meta = MetaStrategy({})
position = None

total_signals = 0
open_long = 0
close_long = 0

regime_counts = {
    "trend": 0,
    "range": 0,
    "expansion": 0,
    "compression": 0
}

strategy_counters = defaultdict(lambda: {"BUY": 0, "SELL": 0})

counter = 0
start = time.time()

checkpoints = [50, 100, 200, 300, 400, 500]

def get_last_debug(meta_obj):
    logger = getattr(meta_obj, "logger", None)
    if logger is None:
        return None
    return getattr(logger, "last_debug", None)

for c in candles:
    counter += 1
    meta.bar_index = counter

    state = meta.compute_meta_state(c)
    decision = meta.compute_meta_signal(state)

    r = meta.local_regime
    if r in regime_counts:
        regime_counts[r] += 1

    last_debug = get_last_debug(meta)

    if decision and isinstance(decision, dict):
        sig = decision.get("signal")
        if sig:
            total_signals += 1
            if sig == "OPEN_LONG":
                open_long += 1
                position = "LONG"
            elif sig == "CLOSE_LONG":
                close_long += 1
                position = None

    if counter in checkpoints:
        print("------------------------------------")
        print("Index:", counter)
        print("Price:", c["close"])
        print("Regime:", meta.local_regime, "/", meta.global_regime)
        print("Position:", position)
        print("Confidence:", state["confidence"])
        print("Momentum:", state["momentum"])
        print("Slope:", state["slope"])
        print("Trend:", state["trend_strength"])
        print("ATR 1h:", state["atr_1h"])
        print("ATR 4h:", state["atr_4h"])
        print("MTF bias 4h:", state["mtf_bias_4h"])

        print("Extended debug:")
        if last_debug is None:
            print("  (no debug info)")
        else:
            dbg = last_debug
            filters = dbg.get("debug", {}).get("filters")
            stage1 = dbg.get("debug", {}).get("stage1")
            stage2 = dbg.get("debug", {}).get("stage2")
            intrabar = dbg.get("debug", {}).get("intrabar_stop")
            soft_exit = dbg.get("debug", {}).get("soft_exit")
            profit_lock = dbg.get("debug", {}).get("profit_lock")
            decision_dbg = dbg.get("decision")

            print("  filters:", filters)
            print("  stage1:", stage1)
            print("  stage2:", stage2)
            print("  intrabar_stop:", intrabar)
            print("  soft_exit:", soft_exit)
            print("  profit_lock:", profit_lock)
            print("  decision:", decision_dbg)

        print("Meta decision:", decision)

print("====================================")
print("Diagnostic summary")
print("Signals:", total_signals)
print("OPEN_LONG:", open_long)
print("CLOSE_LONG:", close_long)
print("Final position:", position)
print("Final regime:", meta.local_regime)
print("====================================")
print("Regime distribution:")
for k in ["trend", "range", "expansion", "compression"]:
    v = regime_counts.get(k, 0)
    pct = (v / total * 100.0) if total > 0 else 0.0
    print(f"  {k:11s}: {v:9d} ({pct:6.2f}%)")

print("====================================")
print("Strategy signal counters")
for name in sorted(strategy_counters.keys()):
    c = strategy_counters[name]
    print(f"{name:25s} BUY: {c['BUY']:6d}  SELL: {c['SELL']:6d}")
print("====================================")
"@

python __meta_debug.py
Remove-Item "__meta_debug.py" -Force
