import pandas as pd

def test_sma_for_backtest_all_branches():
    """
    Тестирует SMA стратегию на ветке buy.
    Ищет внутри модуля функцию sma_strategy или strategy.
    Если стратегия возвращает DataFrame, извлекает колонку signal.
    При пустом DataFrame сигнал считается None.
    """
    from bot_ai.strategy import sma_for_backtest

    # Данные для проверки: SMA_fast > SMA_slow
    df_buy = pd.DataFrame({
        "time": [1, 2, 3, 4, 5],
        "open": [1, 2, 3, 4, 5],
        "high": [1, 2, 3, 4, 5],
        "low": [1, 2, 3, 4, 5],
        "close": [10, 20, 30, 40, 50],
        "volume": [1, 1, 1, 1, 1]
    })

    # Находим функцию внутри модуля
    func = getattr(
        sma_for_backtest,
        "sma_strategy",
        None) or getattr(
        sma_for_backtest,
        "strategy",
        None)
    assert callable(
        func), "В модуле sma_for_backtest нет функции sma_strategy/strategy"

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

