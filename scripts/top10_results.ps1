$resultsPath = "logs/results.csv"

if (-Not (Test-Path $resultsPath)) {
    Write-Host "❌ File not found: $resultsPath"
    exit
}

Import-Csv $resultsPath |
    Sort-Object {[decimal]$_.final_balance} -Descending |
    Select-Object -First 10 |
    Format-Table symbol, timeframe, final_balance, total_trades, win_rate, drawdown -AutoSize
