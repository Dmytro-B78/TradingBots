# scripts/generate_rsi_signals.ps1
# Generate RSI signals for selected pairs and timeframes, with logging

Write-Host "Step 1: Generating RSI signals for TIA, ARB, JTO..."
cd C:\TradingBots\NT
$logPath = "logs/generate_rsi_signals.log"
New-Item -ItemType Directory -Path "logs" -Force | Out-Null
"" | Out-File -FilePath $logPath -Encoding UTF8

$pairs = @("TIAUSDT", "ARBUSDT", "JTOUSDT")
$timeframes = @("1h", "15m")

foreach ($symbol in $pairs) {
    foreach ($timeframe in $timeframes) {
        $csvPath = "data/${symbol}_${timeframe}.csv"
        if (-Not (Test-Path $csvPath)) {
            $msg = "Skipped: missing candles → $csvPath"
            Write-Host $msg
            $msg | Out-File -Append -FilePath $logPath
            continue
        }

        Write-Host "Generating RSI signals: $symbol | $timeframe"
        $result = python -c "
import pandas as pd
import ta
import os
from datetime import datetime, timedelta

symbol = '$symbol'
timeframe = '$timeframe'
log = []

try:
    df = pd.read_csv(f'data/{symbol}_{timeframe}.csv')
    time_col = None
    for col in ['timestamp', 'open_time', 'date', 'time']:
        if col in df.columns:
            time_col = col
            break

    if time_col is None or 'close' not in df.columns:
        log.append(f'ERROR: Missing required columns in {symbol}_{timeframe}')
    else:
        df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
        df['signal'] = 0
        df.loc[df['rsi'] < 30, 'signal'] = 1
        df.loc[df['rsi'] > 70, 'signal'] = -1

        signals = df[[time_col, 'close', 'rsi', 'signal']].dropna()
        signals = signals[signals['signal'] != 0]

        now = datetime.utcnow()
        cutoff = now - timedelta(days=14)
        try:
            signals[time_col] = pd.to_datetime(signals[time_col], unit='ms')
        except:
            signals[time_col] = pd.to_datetime(signals[time_col])

        signals = signals[signals[time_col] >= cutoff]
        os.makedirs('paper_logs', exist_ok=True)
        out_path = f'paper_logs/test_signal_{symbol}_signals.csv'
        signals.to_csv(out_path, index=False)
        log.append(f'Saved: {out_path} ({len(signals)} signals)')
except Exception as e:
    log.append(f'ERROR: {symbol}_{timeframe} → {str(e)}')

for line in log:
    print(line)
" 2>&1

        $result | Out-File -Append -FilePath $logPath
        $result | ForEach-Object { Write-Host $_ }
        Write-Host ""
    }
}

Write-Host "`nLog saved to $logPath"
