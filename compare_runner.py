# compare_runner.py
# Запуск мультипарного бэктеста и сравнения стратегий

from bot_ai.backtest.strategy_comparator import compare_strategies

compare_strategies(
    pairs=["BTCUSDT", "ETHUSDT", "BNBUSDT"],
    strategies=["crossover", "volume_spike"],
    timeframe="1h",
    rsi_threshold=65,
    capital=10000,
    risk_pct=1.0
)
