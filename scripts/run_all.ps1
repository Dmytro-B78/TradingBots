# scripts/run_all.ps1
# Master pipeline: download → move → backtest → analyze

Write-Host "📥 Step 1: Downloading historical candles..."
cd C:\TradingBots\NT
python download_binance.py

Write-Host "`n📂 Step 2: Moving CSV files to data/..."
Move-Item -Path "data/history/*.csv" -Destination "data/" -Force -ErrorAction SilentlyContinue

Write-Host "`n📊 Step 3: Running backtests..."
$csvFiles = Get-ChildItem -Path "data" -Filter "*_*.csv"

foreach ($file in $csvFiles) {
    if ($file.Name -match "^([A-Z0-9]+)_([0-9a-zA-Z]+)\.csv$") {
        $symbol = $matches[1]
        $timeframe = $matches[2]
        Write-Host "▶ Backtest: $symbol | $timeframe"
        python -c "
from bot_ai.backtest.backtest_runner import main
main(capital=10000, risk_pct=0.01, pair='$symbol', timeframe='$timeframe', strategy='rsi', rsi_threshold=50)
"
        Write-Host ""
    }
}

Write-Host "`n📈 Step 4: Opening results.csv (if exists)..."
if (Test-Path "logs/results.csv") {
    Start-Process "logs/results.csv"
} else {
    Write-Host "⚠️ No results.csv found."
}

Write-Host "`n🏆 Step 5: Top 10 strategies by final balance:"
if (Test-Path "logs/results.csv") {
    Import-Csv "logs/results.csv" |
        Sort-Object {[decimal]$_.final_balance} -Descending |
        Select-Object -First 10 |
        Format-Table symbol, timeframe, final_balance, total_trades, win_rate, drawdown -AutoSize
} else {
    Write-Host "⚠️ Skipped: no results to analyze."
}
