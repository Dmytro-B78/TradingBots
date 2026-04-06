# ================================================================
# File: scripts/test_meta_strategy_debug.ps1
# NT-Tech MetaStrategy Diagnostic Tester 3.1 (Fixed)
# - Uses 5m candles by default
# - Calls MetaStrategy.on_candle(candle, position) correctly
# - Maintains local position state (LONG / None)
# - Prints checkpoints with regime + last logged strategy signals
# ASCII-only, deterministic, no Cyrillic
# ================================================================

param(
    [string]$pair = "SOLUSDT-5m.csv"
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

Set-Content -Path __meta_debug.py -Value @"
import os
import time
import csv

from bot_ai.strategy.meta_strategy import MetaStrategy

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

counter = 0
start = time.time()

checkpoints = [
    50000, 100000, 150000, 200000, 250000,
    300000, 350000, 400000, 450000, 500000
]

def get_last_strategy_signals(logger):
    for attr in ["last_strategy_signals", "last_strategy_outputs", "last_signals", "last_strategy_results"]:
        if hasattr(logger, attr):
            v = getattr(logger, attr)
            if v is not None:
                return v
    return None

for c in candles:
    counter += 1

    decision = meta.on_candle(c, position)

    r = getattr(meta, "regime", "unknown")
    if r in regime_counts:
        regime_counts[r] += 1

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

    if counter % 100000 == 0:
        elapsed = time.time() - start
        cps = counter / elapsed if elapsed > 0 else 0.0
        eta = (total - counter) / cps if cps > 0 else 0.0
        print(f"Progress: {counter}/{total} | {cps:.1f} cps | ETA {eta:.1f}s")

    if counter in checkpoints:
        print("------------------------------------")
        print("Index:", counter)
        print("Price:", c["close"])
        print("Regime:", getattr(meta, "regime", None))
        print("Position:", position)

        last = get_last_strategy_signals(meta.logger)
        print("Strategy signals (best-effort):")
        if last is None:
            print("  (no logger field found)")
        else:
            try:
                for item in last:
                    if isinstance(item, (list, tuple)) and len(item) == 3:
                        name, sig, w = item
                        print(" ", name, "=>", sig, "(", w, ")")
                    elif isinstance(item, (list, tuple)) and len(item) == 2:
                        name, out = item
                        print(" ", name, "=>", out)
                    else:
                        print(" ", item)
            except Exception as e:
                print("  (failed to print logger signals)", str(e))

        print("Meta decision:", decision)

print("====================================")
print("Diagnostic summary")
print("Signals:", total_signals)
print("OPEN_LONG:", open_long)
print("CLOSE_LONG:", close_long)
print("Final position:", position)
print("Final regime:", getattr(meta, "regime", None))
print("Regime distribution:")
for k in ["trend", "range", "expansion", "compression"]:
    v = regime_counts.get(k, 0)
    pct = (v / total * 100.0) if total > 0 else 0.0
    print(f"  {k:11s}: {v:9d} ({pct:6.2f}%)")
print("====================================")
"@

python __meta_debug.py
Remove-Item -Path __meta_debug.py -Force
