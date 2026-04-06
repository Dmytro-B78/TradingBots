# ================================================================
# File: scripts/test_backtest_engine.ps1
# NT-Tech Backtester Runner 2.0 (ASCII-only)
# Runs BacktestEngine 4.0 on a CSV file
# ================================================================

param(
    [Parameter(Mandatory = $true)]
    [string]$pair
)

Write-Host "====================================================="
Write-Host "NT-Tech Backtester Runner 2.0"
Write-Host "Engine: BacktestEngine 4.0"
Write-Host "CSV File: $pair"
Write-Host "====================================================="

# Python runner script (inline, ASCII-only)
$runner = @"
import json
from bot_ai.engine.backtest_engine import BacktestEngine

engine = BacktestEngine(initial_balance=10000.0)
result = engine.run(r"$pair")
print(json.dumps(result))
"@

# Save runner to temp file
$tempFile = "$env:TEMP\nt_backtest_runner.py"
Set-Content -Path $tempFile -Value $runner -Encoding ASCII

# Execute Python
Write-Host "Running backtest..."
$json = python $tempFile

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
