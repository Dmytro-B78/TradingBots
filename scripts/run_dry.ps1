python - << "EOF"
from bot_ai.engine.live_engine import LiveEngine
from bot_ai.config.config_loader import ConfigLoader

config = ConfigLoader.load_from_json("config.json")

engine = LiveEngine(
    config=config,
    position_pct=0.25,
    min_volume=50000000,
    dry_run=True
)

engine.run()
EOF
