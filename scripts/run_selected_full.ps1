# scripts/run_selected_full.ps1
# Step-by-step: RSI signal generation → backtest → live execution via Binance Testnet

cd C:\TradingBots\NT
$logPath = "logs/run_selected_full.log"
New-Item -ItemType Directory -Path "logs" -Force | Out-Null
"" | Out-File -FilePath $logPath -Encoding UTF8

$pairs = @("TIAUSDT", "ARBUSDT", "JTOUSDT")
$timeframes = @("1h", "15m")

# Step 1: Generate RSI signals
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
    if 'time' not in df.columns or 'close' not in df.columns:
        log.append(f'ERROR: Missing required columns in {symbol}_{timeframe}')
    else:
        df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
        df['signal'] = ''
        df.loc[df['rsi'] < 30, 'signal'] = 'BUY'
        df.loc[df['rsi'] > 70, 'signal'] = 'SELL'

        signals = df[['time', 'close', 'rsi', 'signal']].dropna()
        signals = signals[signals['signal'] != '']
        signals = signals.rename(columns={'time': 'entry_time', 'close': 'price'})

        signals['entry_time'] = pd.to_datetime(signals['entry_time'], errors='coerce')
        signals = signals.dropna(subset=['entry_time'])
        signals['entry_time'] = (signals['entry_time'].astype('int64') // 10**6)

        now = datetime.utcnow()
        cutoff = int((now - timedelta(days=14)).timestamp() * 1000)
        signals = signals[signals['entry_time'] >= cutoff]

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

# Step 2: Run backtests
Write-Host "`nStep 2: Running backtests..."
foreach ($symbol in $pairs) {
    foreach ($timeframe in $timeframes) {
        $csvPath = "data/${symbol}_${timeframe}.csv"
        $signalPath = "paper_logs/test_signal_${symbol}_signals.csv"

        if (-Not (Test-Path $csvPath)) {
            Write-Host "Skipped: missing candles → $csvPath"
            continue
        }
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

# Step 3: Execute live trades
Write-Host "`nStep 3: Executing live trades..."
foreach ($symbol in $pairs) {
    foreach ($timeframe in $timeframes) {
        $signalPath = "paper_logs/test_signal_${symbol}_signals.csv"
        if (-Not (Test-Path $signalPath)) {
            Write-Host "No signals to execute for $symbol | $timeframe"
            continue
        }

        Write-Host "Executing trade: $symbol | $timeframe"
        python -c "
import pandas as pd
from bot_ai.execution.binance_executor import place_order

symbol = '$symbol'
df = pd.read_csv('$signalPath')
if df.empty:
    print('No signals found.')
else:
    last = df.sort_values('entry_time').iloc[-1]
    side = last['signal'].upper()
    price = float(last['price'])
    qty = 10 / price
    qty = round(qty, 2)

    print(f'Placing {side} order for {qty} {symbol} at ~{price}')
    result = place_order(symbol=symbol, side=side, quantity=qty)
    print('Order result:', result)
" 2>&1
        Write-Host ""
    }
}

# Step 4: Analyze results
Write-Host "`nStep 4: Analyzing results..."
if (Test-Path "logs/results.csv") {
    Start-Process "logs/results.csv"
    Import-Csv "logs/results.csv" |
        Where-Object { [int]$_.total_trades -ge 1 } |
        Sort-Object {[decimal]$_.final_balance} -Descending |
        Select-Object -First 10 |
        Tee-Object -Variable top10 |
        Format-Table symbol, timeframe, final_balance, total_trades, win_rate, drawdown -AutoSize

    $top10 | Export-Csv -Path "logs/top10.csv" -NoTypeInformation
    Write-Host "`nExported top 10 to logs/top10.csv"
} else {
    Write-Host "No results.csv found. Skipping analysis."
}
