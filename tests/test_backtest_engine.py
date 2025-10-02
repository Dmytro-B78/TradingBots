import pandas as pd

def test_backtest_engine_empty_and_with_data(monkeypatch, tmp_path):
    from bot_ai.backtest import backtest_engine

    # Фиктивный cfg
    cfg = type("Cfg", (), {})()
    cfg.exchange = "binance"

    # 1. Пустые пары → сразу return
    result_empty = backtest_engine.run_backtest(cfg, [], lambda df: None, "SMA", days=1, timeframes=["1h"])
    assert result_empty is None

    # 2. Мокаем ccxt.binance
    class DummyExchange:
        def parse8601(self, s): return 0
        def fetch_ohlcv(self, symbol, timeframe, since, limit):
            return [
                [1, 10, 12, 9, 11, 100],
                [2, 11, 13, 10, 12, 150]
            ]
    monkeypatch.setattr(backtest_engine.ccxt, "binance", lambda *a, **k: DummyExchange())

    # Мокаем RiskGuard, PositionSizer, DynamicSLTP
    monkeypatch.setattr(backtest_engine, "RiskGuard", lambda cfg: type("RG", (), {
        "can_open_trade": lambda self, sym: True,
        "register_trade": lambda self, sym, trade: None
    })())
    monkeypatch.setattr(backtest_engine, "PositionSizer", lambda cfg: type("PS", (), {
        "calculate": lambda self, sym, trade: 1.0
    })())
    monkeypatch.setattr(backtest_engine, "DynamicSLTP", lambda cfg: type("DS", (), {
        "calculate": lambda self, df, trade: (90.0, 110.0)
    })())

    # Стратегия возвращает DataFrame с одной сделкой
    trades_df = pd.DataFrame([{"Profit(%)": 5}])
    strategy_func = lambda df: trades_df

    # 3. Запуск с одной парой
    result = backtest_engine.run_backtest(cfg, ["BTC/USDT"], strategy_func, "SMA", days=1, timeframes=["1h"])
    assert result is None or isinstance(result, type(None))
