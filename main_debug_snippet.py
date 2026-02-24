# Фрагмент main.py с отладкой simulate_trading()

def simulate_trading(df, strategy, symbol, balance=1000):
    df = strategy.calculate_indicators(df)
    df = strategy.generate_signals(df)

    print("\n🧪 Последние сигналы:")
    print(df[["time", "close", "high_roll", "low_roll", "signal"]].tail(10))

    strategy.backtest(df, initial_balance=balance)
    summary = strategy.summary(symbol)

    print("\n📈 Последние строки отчёта:")
    print(summary.tail(5))

    return summary
