import importlib.util
import pathlib
import sys

import pytest

def test_cli_entrypoint_runs(monkeypatch):
    script_path = pathlib.Path(__file__).parent.parent / "main.py"
    if not script_path.exists():
        pytest.skip("main.py не найден, CLI-тест пропущен")

    # Мокаем time.sleep, чтобы выйти из цикла сразу
    import time
    monkeypatch.setattr(
        time, "sleep", lambda s: (
            _ for _ in ()).throw(
            SystemExit()))

    # Мокаем select_pairs, чтобы вернуть одну фиктивную пару
    import bot_ai.selector.pipeline as pipeline
    monkeypatch.setattr(pipeline, "select_pairs", lambda *a, **k: ["BTC/USDT"])

    # Мокаем ccxt.binance, чтобы не ходить в сеть
    import ccxt
    monkeypatch.setattr(ccxt,
                        "binance",
                        lambda *a,
                        **k: type("E",
                                  (),
                                  {"fetch_ticker": lambda self,
                                   sym: {"last": 100},
                                      "fetch_ohlcv": lambda self,
                                      sym,
                                      timeframe,
                                      limit: [[None,
                                               None,
                                               None,
                                               None,
                                               100,
                                               None]]})())

    # Мокаем TradeExecutor, чтобы не падать на лишних аргументах
    import bot_ai.exec.executor as executor_mod

    class DummyExecutor:
        def __init__(self, *a, **k):
            self.positions = {}

        def execute_trade(self, *a, **k):
            pass
    monkeypatch.setattr(executor_mod, "TradeExecutor", DummyExecutor)

    # Импортируем main.py в текущем процессе, чтобы моки работали
    spec = importlib.util.spec_from_file_location("main", script_path)
    main_module = importlib.util.module_from_spec(spec)
    sys.modules["main"] = main_module

    # Запуск main.py — ожидаем SystemExit из-за замоканного sleep
    with pytest.raises(SystemExit):
        spec.loader.exec_module(main_module)

