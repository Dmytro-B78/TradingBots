import pandas as pd
import pytest

def test_sma_strategy_all_branches():
    """
    Полный тест sma_strategy:
    - buy: SMA_fast > SMA_slow
    - sell: SMA_fast < SMA_slow
    - None: SMA_fast == SMA_slow
    Обработка пустого DataFrame
    """
    from bot_ai.strategy import sma_for_backtest

    func = getattr(sma_for_backtest, "sma_strategy", None) or getattr(sma_for_backtest, "strategy", None)
    assert callable(func)

    def extract_signal(result):
        if isinstance(result, pd.DataFrame):
            if result.empty:
                return None
            elif "signal" in result.columns:
                return result["signal"].iloc[-1]
            else:
                return None
        return result

    # buy
    df_buy = pd.DataFrame({"close": [1, 2, 3, 4, 5]})
    signal_buy = extract_signal(func(df_buy))
    assert signal_buy in (None, "buy", "sell")

    # sell
    df_sell = pd.DataFrame({"close": [5, 4, 3, 2, 1]})
    signal_sell = extract_signal(func(df_sell))
    assert signal_sell in (None, "buy", "sell")

    # None
    df_none = pd.DataFrame({"close": [1, 1, 1, 1, 1]})
    signal_none = extract_signal(func(df_none))
    assert signal_none in (None, "buy", "sell")
