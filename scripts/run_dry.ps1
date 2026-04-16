# ================================================================
# NT-Tech LiveEngine Dry Runner
# ASCII-only, no Cyrillic
# LiveEngine 4.3 uses on_candle() only
# ================================================================

Write-Host "Starting NT-Tech LiveEngine (DRY MODE)..."

$env:PYTHONPATH = "C:\TradingBots\NT"

$temp = "__run_dry.py"

Set-Content -Path $temp -Value @"
import json
import csv
from bot_ai.engine.live_engine import LiveEngine

config_path = r"C:\TradingBots\NT\config.json"
candles_path = r"C:\TradingBots\candles\compiled\SOLUSDT-1h-2026-03.csv"

# Load config
with open(config_path, "r") as f:
    config = json.load(f)

# Force dry mode
config["live"]["dry_run"] = True
config["live"]["api_enabled"] = False
config["live"]["allow_live_trading"] = False

engine = LiveEngine(config=config)

# Load candles
candles = []
with open(candles_path, "r") as f:
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

for i, c in enumerate(candles):
    engine.on_candle("SOLUSDT", c)
    if i % 5000 == 0:
        print("Progress:", i)

print("Dry run completed.")
"@ -Encoding ASCII

python $temp
Remove-Item $temp -Force

Write-Host "Dry-mode LiveEngine finished."
