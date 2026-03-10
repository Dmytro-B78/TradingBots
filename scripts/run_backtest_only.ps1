# scripts/run_backtest_only.ps1
# Run backtests only (no candle download), log results, export top 10

Write-Host "Step 1: Running backtests from data/*.csv..."
cd C:\TradingBots\NT
$csvFiles = Get-ChildItem -Path "data" -Filter "*_*.csv"

foreach ($file in $csvFiles) {
    if ($file.Name -match "^([A-Z0-9]+)_([0-9a-zA-Z]+)\.csv$") {
        $symbol = $matches[1]
        $timeframe = $matches[2]
        $signalPath = "paper_logs/test_signal_${symbol}_signals.csv"

        if (-Not (Test-Path $signalPath)) {
            Write-Host "Skipped: no signals → $signalPath"
            continue
        }

        Write-Host "Backtest: $symbol | $timeframe"
        python -c "
from bot_ai.backtest.backtest_runner import main
main(capital=10000, risk_pct=0.01, pair='$symbol', timeframe='$timeframe', strategy='rsi', rsi_threshold=50)
"
        Write-Host ""
    }
}

Write-Host "`nStep 2: Opening results.csv (if exists)..."
if (Test-Path "logs/results.csv") {
    Start-Process "logs/results.csv"
} else {
    Write-Host "No results.csv found."
}

Write-Host "`nStep 3: Top 10 strategies by final balance:"
if (Test-Path "logs/results.csv") {
    Import-Csv "logs/results.csv" |
        Where-Object { [int]$_.total_trades -ge 1 } |
        Sort-Object {[decimal]$_.final_balance} -Descending |
        Select-Object -First 10 |
        Tee-Object -Variable top10 |
        Format-Table symbol, timeframe, final_balance, total_trades, win_rate, drawdown -AutoSize

    $top10 | Export-Csv -Path "logs/top10.csv" -NoTypeInformation
    Write-Host "`nExported top 10 to logs/top10.csv"
} else {
    Write-Host "Skipped: no results to analyze."
}
