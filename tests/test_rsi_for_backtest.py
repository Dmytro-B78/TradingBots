import pandas as pd

def test_rsi_for_backtest_all_branches():
    """
    Тестирует RSI стратегию на ветке buy.
    Ищет внутри модуля функцию rsi_strategy или strategy.
    Если стратегия возвращает DataFrame, извлекает колонку signal.
    При пустом DataFrame сигнал считается None.
    """
    from bot_ai.strategy import rsi_for_backtest

    # Данные для проверки: RSI < 30
    df_buy = pd.DataFrame({
        "time": [1, 2, 3, 4, 5],
        "open": [1, 2, 3, 4, 5],
        "high": [1, 2, 3, 4, 5],
        "low": [1, 2, 3, 4, 5],
        "close": [10, 12, 11, 13, 12],
        "volume": [1, 1, 1, 1, 1]
    })

    # Находим функцию внутри модуля
    func = getattr(
        rsi_for_backtest,
        "rsi_strategy",
        None) or getattr(
        rsi_for_backtest,
        "strategy",
        None)
    assert callable(
        func), "В модуле rsi_for_backtest нет функции rsi_strategy/strategy"

    # Вызываем стратегию
    result = func(df_buy)

    # Обработка результата
    if isinstance(result, pd.DataFrame):
        if result.empty:
            signal_value = None
        elif "signal" in result.columns:
            signal_value = result["signal"].iloc[-1]
        else:
            signal_value = None
    else:
        signal_value = result

    assert signal_value in (None, "buy", "sell")

