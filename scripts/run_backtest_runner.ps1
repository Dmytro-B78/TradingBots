\ = Get-ChildItem -Path "C:\TradingBots\NT\data" -Filter "*_*.csv"

foreach (\ in \) {
    if (\.Name -match "^([A-Z0-9]+)_([0-9a-zA-Z]+)\.csv\$") {
        \ = \[1]
        \ = \[2]
        Write-Host "▶ Running backtest_runner.py for \ | \"
        python -c \"
from bot_ai.backtest.backtest_runner import main
main(capital=10000, risk_pct=0.01, pair='\', timeframe='\', strategy='rsi', rsi_threshold=50)
\"
        Write-Host ""
    }
}
