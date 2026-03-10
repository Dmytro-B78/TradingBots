# ============================================
# File: run_daily_rsi_job.ps1
# Purpose: Daily execution of RSI optimization and simulation
# Schedule: To be run via Windows Task Scheduler
# ============================================

# === Set working directory ===
Set-Location "C:\TradingBots\NT"

# === Set PYTHONPATH to project root ===
$env:PYTHONPATH = "C:\TradingBots\NT"

# === Define symbol and timeframe ===
$symbol = "BTCUSDT"
$timeframe = "1h"

# === Run optimization and simulation ===
python bot_ai\backtest\optimize_rsi_grid.py --symbol $symbol --timeframe $timeframe
