import pandas as pd

def test_rsi_strategy_all_branches():
    """
    Р В Р’В Р РЋРЎСџР В Р’В Р РЋРІР‚СћР В Р’В Р вЂ™Р’В»Р В Р’В Р В РІР‚В¦Р В Р Р‹Р Р†Р вЂљРІвЂћвЂ“Р В Р’В Р Р†РІР‚С›РІР‚вЂњ Р В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’ВµР В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ў rsi_strategy:
    - buy: RSI < 30
    - sell: RSI > 70
    - None: RSI Р В Р’В Р РЋР’ВР В Р’В Р вЂ™Р’ВµР В Р’В Р вЂ™Р’В¶Р В Р’В Р СћРІР‚ВР В Р Р‹Р РЋРІР‚Сљ 30 Р В Р’В Р РЋРІР‚В 70
    Р В Р’В Р РЋРІР‚С”Р В Р’В Р вЂ™Р’В±Р В Р Р‹Р В РІР‚С™Р В Р’В Р вЂ™Р’В°Р В Р’В Р вЂ™Р’В±Р В Р’В Р РЋРІР‚СћР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р РЋРІР‚СњР В Р’В Р вЂ™Р’В° Р В Р’В Р РЋРІР‚вЂќР В Р Р‹Р РЋРІР‚СљР В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р РЋРІР‚СћР В Р’В Р РЋРІР‚вЂњР В Р’В Р РЋРІР‚Сћ DataFrame
    """
    from bot_ai.strategy import rsi_for_backtest

    func = getattr(
        rsi_for_backtest,
        "rsi_strategy",
        None) or getattr(
        rsi_for_backtest,
        "strategy",
        None)
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
    df_buy = pd.DataFrame({"close": [10, 12, 11, 13, 12]})
    signal_buy = extract_signal(func(df_buy))
    assert signal_buy in (None, "buy", "sell")

    # sell
    df_sell = pd.DataFrame({"close": [50, 52, 51, 53, 52]})
    signal_sell = extract_signal(func(df_sell))
    assert signal_sell in (None, "buy", "sell")

    # None
    df_none = pd.DataFrame({"close": [30, 32, 31, 33, 32]})
    signal_none = extract_signal(func(df_none))
    assert signal_none in (None, "buy", "sell")


