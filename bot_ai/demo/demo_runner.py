# demo_runner.py
# Назначение: Демонстрация стратегии на исторических данных
# Структура:
# └── bot_ai/demo/demo_runner.py

from bot_ai.selector.selector_engine import run_selector
from bot_ai.exchange.data_loader import load_ohlcv
from bot_ai.analytics.metrics_calculator import calculate_metrics
from bot_ai.diagnostics.debug_tools import plot_equity_curve

def main():
    symbol = "BTC/USDT"
    df = load_ohlcv(symbol, limit=300)
    config = {
        "strategies": ["sma"],
        "sma_fast": 5,
        "sma_slow": 20,
        "stop_loss_pct": 0.02,
        "min_risk_reward_ratio": 1.5,
        "capital": 10000
    }

    trades = run_selector(symbol, df, config)
    metrics = calculate_metrics(trades, config["capital"])
    print(metrics)
    plot_equity_curve(metrics["equity_curve"])

if __name__ == "__main__":
    main()
