# -*- coding: utf-8 -*-
# ============================================
# File: backtester.py
# Назначение: Упрощённый бэктестинг стратегий на исторических данных
# Используется для оценки поведения стратегии на прошлых свечах
# ============================================

def backtest(strategy_fn, pair, timeframe, fetch_ohlcv):
    """
    Выполняет бэктест стратегии на исторических данных.

    :param strategy_fn: функция стратегии, принимающая DataFrame и возвращающая сигнал
    :param pair: торговая пара (например, 'BTC/USDT')
    :param timeframe: таймфрейм (например, '1h', '4h')
    :param fetch_ohlcv: функция загрузки исторических данных
    :return: список сигналов по мере их генерации
    """
    df = fetch_ohlcv(pair, timeframe=timeframe)
    if df is None or df.empty:
        return None

    signals = []
    for i in range(50, len(df)):
        sub_df = df.iloc[:i].copy()
        signal = strategy_fn(sub_df)
        signals.append(signal)

    return signals
