# ================================================================
# NT-Tech Live Engine Launcher (REAL MODE)
# ASCII-only, no Cyrillic
# ================================================================

Write-Host "Starting NT-Tech LiveEngine (REAL MODE)..."

$env:PYTHONPATH = "C:\TradingBots\NT"

python - << 'EOF'
import json
import sys
from bot_ai.engine.live_engine import LiveEngine

config_path = r"C:\TradingBots\NT\config.json"

with open(config_path, "r") as f:
    config = json.load(f)

# Safety checks
live_cfg = config.get("live", {})

if live_cfg.get("allow_live_trading", False) is False:
    print("ERROR: allow_live_trading = false. Real trading is blocked.")
    sys.exit(1)

if live_cfg.get("api_enabled", False) is False:
    print("ERROR: api_enabled = false. Exchange API is disabled.")
    sys.exit(1)

if live_cfg.get("dry_run", True) is True:
    print("ERROR: dry_run = true. Real trading is disabled.")
    sys.exit(1)

if live_cfg.get("require_manual_confirm", True):
    print("Manual confirmation required to start REAL MODE.")
    print("Type YES to continue:")
    user_input = sys.stdin.readline().strip()
    if user_input != "YES":
        print("Aborted by user.")
        sys.exit(1)

engine = LiveEngine(config=config)
engine.run()
EOF

Write-Host "LiveEngine finished."
