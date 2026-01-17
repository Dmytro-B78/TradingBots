# backtest_runner.py
# Назначение: Запуск бэктеста по стратегии SMA + RSI + ATR + ADX
# Структура:
# └── bot_ai/backtest/backtest_runner.py

from bot_ai.exchange.data_loader import load_ohlcv
from bot_ai.selector.selector_engine import run_selector
from bot_ai.analytics.metrics_calculator import calculate_metrics
from bot_ai.analytics.report_generator import generate_report

def main():
    symbol = "BTC/USDT"
    df = load_ohlcv(symbol, timeframe="1h", limit=200)

    config = {
        "strategies": ["sma", "rsi", "adx", "atr"],
        "sma_fast": 5,
        "sma_slow": 10,
        "rsi_period": 14,
        "rsi_buy_threshold": 65,
        "rsi_sell_threshold": 70,
        "adx_period": 14,
        "adx_threshold": 18,
        "atr_period": 14,
        "atr_threshold": 0.01,
        "stop_loss_pct": 0.02,
        "trailing_stop_pct": 0.015,
        "min_risk_reward_ratio": 1.5,
        "max_holding_period": 48,
        "capital": 10000,
        "risk_per_trade": 0.01
    }

    trades = run_selector(symbol, df, config)
    metrics = calculate_metrics(trades, capital=config["capital"])
    report = generate_report(metrics)

    print(report)
