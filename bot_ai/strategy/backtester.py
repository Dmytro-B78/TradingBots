# bot_ai/strategy/backtester.py
# Бэктестинг стратегии на исторических данных

def backtest(strategy_fn, pair, timeframe, fetch_ohlcv):
    df = fetch_ohlcv(pair, timeframe=timeframe)
    if df is None or df.empty:
        return None

    signals = []
    for i in range(50, len(df)):
        sub_df = df.iloc[:i].copy()
        signal = strategy_fn(sub_df)
        signals.append(signal)
    return signals

