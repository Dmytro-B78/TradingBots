# ================================================================
# NT-Tech Backtest Engine Tester
# ASCII-only, no Cyrillic
# Runs BacktestEngine on a single CSV pair
# ================================================================

param(
    [Parameter(Mandatory = $true)]
    [string]$pair
)

Write-Host "====================================================="
Write-Host "NT-Tech Backtest Engine Tester"
Write-Host ("Pair: {0}" -f $pair)
Write-Host "====================================================="

$env:PYTHONPATH = "C:\TradingBots\NT"

python - << 'EOF'
import json
import os
import sys
from bot_ai.backtest.backtest_engine import BacktestEngine

# Read pair from PowerShell argument
pair = sys.argv[1]

csv_path = f"C:/TradingBots/candles/compiled/{pair}-1h.csv"

if not os.path.exists(csv_path):
    print(f"CSV file not found: {csv_path}")
    sys.exit(1)

engine = BacktestEngine(
    symbol=pair,
    interval="1h",
    start_date=None,
    end_date=None,
    initial_balance=10000.0,
    strategy=None
)

result = engine.run(csv_path)

print(json.dumps(result))
EOF $pair

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Python execution failed."
    exit
}

$result = $json | ConvertFrom-Json

Write-Host "====================================================="
Write-Host "Backtest Summary"
Write-Host "====================================================="
Write-Host ("Initial Balance : {0}" -f $result.initial_balance)
Write-Host ("Final Balance   : {0}" -f $result.final_balance)
Write-Host ("Net Profit      : {0}" -f $result.net_profit)
Write-Host ("Trades          : {0}" -f $result.trades)
Write-Host ("Wins            : {0}" -f $result.wins)
Write-Host ("Losses          : {0}" -f $result.losses)
Write-Host ("Winrate (%)     : {0}" -f $result.winrate_pct)
Write-Host ("Max Drawdown    : {0}" -f $result.max_drawdown)
Write-Host "====================================================="
Write-Host "Done."
