# ================================================================
# NT-Tech test_meta_strategy.ps1
# MetaStrategy tester (ASCII-only)
# No Cyrillic, no nested here-strings
# ================================================================

Write-Host "Testing MetaStrategy on dataset..."
Write-Host "============================================"

$temp = "__meta_test.py"

Set-Content -Path $temp -Value @"
import os
import time
import csv
from bot_ai.strategy.meta_strategy import MetaStrategy

folder = r'C:\\TradingBots\\candles\\compiled'
files = [
    'SOLUSDT-1m.csv'
]

for fname in files:
    path = os.path.join(folder, fname)
    print("====================================")
    print("Testing:", fname)
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

    open_long = 0
    close_long = 0
    total_signals = 0

    counter = 0
    start = time.time()

    for c in candles:
        counter += 1

        if counter % 10000 == 0:
            elapsed = time.time() - start
            cps = counter / elapsed
            eta = (total - counter) / cps
            print(f"Progress: {counter}/{total} | {cps:.1f} cps | ETA {eta:.1f}s")

        sig = meta.on_candle(c)

        if sig:
            total_signals += 1
            if sig.get("signal") == "OPEN_LONG":
                open_long += 1
            if sig.get("signal") == "CLOSE_LONG":
                close_long += 1

    print("====================================")
    print("Signals:", total_signals)
    print("OPEN_LONG:", open_long)
    print("CLOSE_LONG:", close_long)
    print("Final regime:", meta.regime)
    print("====================================")
"@ -Encoding ASCII

python $temp
Remove-Item $temp -Force
