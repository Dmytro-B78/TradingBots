# Create scripts directory if it doesn't exist
if (-not (Test-Path "C:\TradingBots\NT\scripts")) {
    New-Item -Path "C:\TradingBots\NT\scripts" -ItemType Directory | Out-Null
}

# Script: run_download.ps1
@"
cd C:\TradingBots\NT
python download_binance.py
"@ | Set-Content -Path "C:\TradingBots\NT\scripts\run_download.ps1" -Encoding UTF8

# Script: move_history_to_data.ps1
@"
Move-Item -Path "data/history/*.csv" -Destination "data/" -Force
"@ | Set-Content -Path "C:\TradingBots\NT\scripts\move_history_to_data.ps1" -Encoding UTF8

# Script: run_backtest_runner.ps1
@"
\$csvFiles = Get-ChildItem -Path "C:\TradingBots\NT\data" -Filter "*_*.csv"

foreach (\$file in \$csvFiles) {
    if (\$file.Name -match "^([A-Z0-9]+)_([0-9a-zA-Z]+)\.csv\$") {
        \$symbol = \$matches[1]
        \$timeframe = \$matches[2]
        Write-Host "▶ Running backtest_runner.py for \$symbol | \$timeframe"
        python -c \"
from bot_ai.backtest.backtest_runner import main
main(capital=10000, risk_pct=0.01, pair='\$symbol', timeframe='\$timeframe', strategy='rsi', rsi_threshold=50)
\"
        Write-Host ""
    }
}
"@ | Set-Content -Path "C:\TradingBots\NT\scripts\run_backtest_runner.ps1" -Encoding UTF8
