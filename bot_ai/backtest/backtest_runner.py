# bot_ai/backtest/backtest_runner.py
# Точка входа для запуска бэктеста из CLI

from bot_ai.backtest.backtest_engine import run_backtest

def main(capital=10000, risk_pct=0.01):
    # Параметры стратегии (можно расширить)
    pair = "AVAXUSDT"
    timeframe = "1h"
    strategy = "rsi"
    rsi_threshold = 50

    # Запуск бэктеста
    report = run_backtest(
        pair=pair,
        timeframe=timeframe,
        strategy=strategy,
        rsi_threshold=rsi_threshold,
        capital=capital,
        risk_pct=risk_pct
    )

    # Вывод отчёта
    print("Backtest Report")
    print("-------------------------")
    for key, value in report.items():
        if isinstance(value, float):
            if "capital" in key.lower():
                print(f"{key.replace('_', ' ').title()}: ${value:,.2f}")
            else:
                print(f"{key.replace('_', ' ').title()}: {value}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
