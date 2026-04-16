# ================================================================
# NT-Tech Strategy Optimizer Launcher
# ASCII-only, no Cyrillic
# ================================================================

Write-Host "Starting NT-Tech Optimizer..."

$env:PYTHONPATH = "C:\TradingBots\NT"

python - << 'EOF'
import json
from bot_ai.backtest.night_backtest import run_night_backtest

config_path = r"C:\TradingBots\NT\config.json"

with open(config_path, "r") as f:
    config = json.load(f)

# Enable optimizer mode
if "optimizer" not in config:
    config["optimizer"] = {}

config["optimizer"]["enabled"] = True

# Run optimization
run_night_backtest(config)
EOF

Write-Host "Optimizer finished."
