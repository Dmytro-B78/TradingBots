# ============================================
# File: backtest.py
# Purpose: Обёртка для запуска стратегии на тестовых данных
# ============================================

import pandas as pd
from bot_ai.strategy.mean_reversion import MeanReversionStrategy

def run_backtest(symbol, candles, strategy_params):
    """
    Запускает стратегию на тестовых данных и возвращает метрики.

    Параметры:
    - symbol: тикер (например, "BTCUSDT")
    - candles: список словарей с OHLCV-данными
    - strategy_params: dict с параметрами стратегии

    Возвращает:
    - dict с total_pnl, num_trades и другими метриками
    """
    df = pd.DataFrame(candles)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    df.sort_index(inplace=True)

    config = strategy_params.copy()
    config["external_data"] = candles  # если стратегия требует

    strategy = MeanReversionStrategy(config)
    df = strategy.calculate_indicators(df)
    df = strategy.generate_signals(df)
    strategy.backtest(df)
    trades = strategy.summary(symbol)

    total_pnl = trades["pnl"].sum() if not trades.empty else 0
    num_trades = len(trades)

    return {
        "total_pnl": round(total_pnl, 2),
        "num_trades": num_trades
    }
