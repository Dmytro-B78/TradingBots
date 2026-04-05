Write-Host "Starting NT-Tech LiveEngine (REAL MODE)..."

python - << 'EOF'
from bot_ai.engine.live_engine import LiveEngine
from bot_ai.engine.config_loader import ConfigLoader

config = ConfigLoader.load_from_json("config.json")
engine = LiveEngine(config, dry_run=False)
engine.run()
EOF
