Write-Host "=== Ночной бэктест NeuroTrade ===" -ForegroundColor Cyan

$projectRoot = "C:\TradingBots\NT"
cd $projectRoot

& .\.venv\Scripts\Activate.ps1

python scripts/night_backtest.py
