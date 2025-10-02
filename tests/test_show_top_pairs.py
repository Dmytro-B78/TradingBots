import logging
import pytest

def test_show_top_pairs_all_branches(monkeypatch, caplog):
    """
    Полный тест всех веток show_top_pairs:
    - пустой список пар
    - успешный fetch_ticker
    - исключение в fetch_ticker
    - сортировка и вывод топ-N
    """
    from bot_ai.selector.pipeline import show_top_pairs

    caplog.set_level(logging.INFO)

    # --- 1. Пустой список ---
    cfg = type("Cfg", (), {"exchange": "binance"})
    caplog.clear()
    show_top_pairs(cfg, [])
    assert any("Whitelist пуст." in m for m in caplog.messages)

    # --- 2. Непустой список ---
    # Мокаем ccxt.binance
    class DummyExchange:
        def __init__(self, *a, **k): pass
        def fetch_ticker(self, symbol):
            if symbol == "BAD/USDT":
                raise Exception("fail")
            return {"quoteVolume": 1000 if symbol == "AAA/USDT" else 500}

    monkeypatch.setattr("bot_ai.selector.pipeline.ccxt.binance", DummyExchange)

    pairs = ["AAA/USDT", "BBB/USDT", "BAD/USDT"]
    caplog.clear()
    show_top_pairs(cfg, pairs, top_n=2)

    # Проверяем, что AAA и BBB попали в лог, BAD пропущен
    msgs = "\n".join(caplog.messages)
    assert "AAA/USDT" in msgs
    assert "BBB/USDT" in msgs
    assert "BAD/USDT" not in msgs
    assert any("Топ-2 пар" in m for m in caplog.messages)
