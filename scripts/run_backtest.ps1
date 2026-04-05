# ================================================================
# NT-Tech Backtest Engine Launcher
# ASCII-only, no Cyrillic
# ================================================================

Write-Host "Starting NT-Tech Backtest Engine..."

$env:PYTHONPATH = "C:\TradingBots\NT"

python - << "EOF"
from bot_ai.engine.backtest_engine import BacktestEngine
from bot_ai.strategy.strategy_manager import StrategyManager
import json

config_path = r"C:\TradingBots\NT\bot_ai\config\backtest_config.json"

with open(config_path, "r") as f:
    cfg = json.load(f)

strategy = StrategyManager.load(cfg["strategy"]["name"], cfg["strategy"]["params"])

engine = BacktestEngine(
    symbol=cfg["symbol"],
    interval=cfg["interval"],
    start_date=cfg["start_date"],
    end_date=cfg["end_date"],
    initial_balance=cfg["initial_balance"],
    strategy=strategy
)

engine.run()
EOF

Write-Host "Backtest Engine finished."
