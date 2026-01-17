# backtest_runner.py
# Запуск бэктеста стратегии

from bot_ai.backtest.simulator import simulate

simulate(
    pair="BTCUSDT",
    timeframe="1h",
    strategy="volume_spike",
    rsi_threshold=65,
    capital=10000,
    risk_pct=1.0
)
