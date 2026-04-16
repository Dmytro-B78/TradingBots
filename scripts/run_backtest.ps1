# ================================================================
# NT-Tech Backtest Runner (2026 Edition)
# File: C:\TradingBots\NT\scripts\run_backtest.ps1
#
# Purpose:
#   Launches the NT-Tech night_backtest engine using the modern
#   accelerated backtest pipeline:
#       - fast_backtest
#       - analyzer 2.2
#       - selector ranker
#       - NT-Tech scoring model
#
# Description:
#   This script sets PYTHONPATH to the NT project root and executes
#   night_backtest.py, which performs:
#       - multi-symbol backtesting
#       - scoring and ranking
#       - PnL, DD, PF, WR metrics
#       - equity and trade analysis
#
# Notes:
#   - ASCII-only, no Cyrillic
#   - Requires Python 3.10+
#   - Uses config.json from project root
# ================================================================

Write-Host "Starting NT-Tech Backtest..."

$env:PYTHONPATH = "C:\TradingBots\NT"

python "C:\TradingBots\NT\bot_ai\backtest\night_backtest.py"

Write-Host "Backtest finished."
