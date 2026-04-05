# ================================================================
# NT-Tech Strategy Optimizer Launcher
# ASCII-only, no Cyrillic
# ================================================================

Write-Host "Starting NT-Tech Optimizer..."

$env:PYTHONPATH = "C:\TradingBots\NT"

python - << "EOF"
from bot_ai.engine.optimizer_engine import OptimizerEngine
from bot_ai.strategy.strategy_manager import StrategyManager
import json

config_path = r"C:\TradingBots\NT\bot_ai\config\backtest_config.json"

with open(config_path, "r") as f:
    cfg = json.load(f)

base_strategy = StrategyManager.load(cfg["strategy"]["name"], cfg["strategy"]["params"])

optimizer = OptimizerEngine(
    symbol=cfg["symbol"],
    interval=cfg["interval"],
    start_date=cfg["start_date"],
    end_date=cfg["end_date"],
    initial_balance=cfg["initial_balance"],
    base_strategy=base_strategy
)

optimizer.run()
EOF

Write-Host "Optimizer finished."
# ================================================================
# NT-Tech Strategy Optimizer Launcher
# ASCII-only, no Cyrillic
# ================================================================

Write-Host "Starting NT-Tech Optimizer..."

$env:PYTHONPATH = "C:\TradingBots\NT"

python - << "EOF"
from bot_ai.engine.optimizer_engine import OptimizerEngine
from bot_ai.strategy.strategy_manager import StrategyManager
import json

config_path = r"C:\TradingBots\NT\bot_ai\config\optimizer_config.json"

with open(config_path, "r") as f:
    cfg = json.load(f)

strategy_cfg = cfg["optimizer"]["strategy"]
base_strategy = StrategyManager.load(strategy_cfg["name"], strategy_cfg["params"])

optimizer = OptimizerEngine(
    symbol=cfg["optimizer"]["symbol"],
    interval=cfg["optimizer"]["interval"],
    start_date=cfg["optimizer"]["start_date"],
    end_date=cfg["optimizer"]["end_date"],
    initial_balance=cfg["optimizer"]["initial_balance"],
    base_strategy=base_strategy
)

optimizer.run()
EOF

Write-Host "Optimizer finished."
