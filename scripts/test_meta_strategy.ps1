Write-Host "Testing MetaStrategy 2.5 on real candles..."

$temp = "__meta_test.py"

$code = @"
import os
import time
from bot_ai.engine.data_loader import DataLoader
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

    candles = DataLoader.load(path)
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

        # progress every 10k candles
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

    print("Signals:", total_signals)
    print("OPEN_LONG:", open_long)
    print("CLOSE_LONG:", close_long)
"@

Set-Content -Path $temp -Value $code
python $temp
Remove-Item $temp -Force
