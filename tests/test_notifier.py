import pytest
from bot_ai.utils.notifier import Notifier
from types import SimpleNamespace

def make_cfg(enabled=True):
    return SimpleNamespace(
        enabled=enabled,
        provider="telegram",
        telegram_token="T",
        telegram_chat_id="C"
    )

def test_send_success(monkeypatch):
    cfg = make_cfg()
    notifier = Notifier(cfg)
    called = {}

    def fake_post(url, **kwargs):
        called["url"] = url
        called["json"] = kwargs.get("json", {})

        class Resp:
            status_code = 200
            text = "OK"
            def raise_for_status(self): pass
        return Resp()

    monkeypatch.setattr("bot_ai.utils.notifier.requests.post", fake_post)
    notifier.send("hello")
    assert called["json"]["text"] == "hello"
    assert "chat_id" in called["json"]

def test_send_empty_disabled(monkeypatch):
    cfg = make_cfg(enabled=False)
    notifier = Notifier(cfg)
    called = {}

    def fake_post(url, **kwargs):
        called["called"] = True
        class Resp:
            status_code = 200
            text = "OK"
            def raise_for_status(self): pass
        return Resp()

    monkeypatch.setattr("bot_ai.utils.notifier.requests.post", fake_post)
    notifier.send("should not send")
    assert "called" not in called  # send should not be called

def test_trade_open(monkeypatch):
    cfg = make_cfg()
    notifier = Notifier(cfg)
    sent = {}

    monkeypatch.setattr(notifier, "send", lambda msg: sent.setdefault("msg", msg))

    trade_data = {
        "Symbol": "BTCUSDT",
        "Side": "buy",
        "Price": 50000,
        "PositionSize": 0.1,
        "SL": 49000,
        "TP": 52000
    }
    notifier.trade_open(trade_data)
    assert "Открыта сделка" in sent["msg"]
    assert "BTCUSDT" in sent["msg"]

def test_trade_close(monkeypatch):
    cfg = make_cfg()
    notifier = Notifier(cfg)
    sent = {}

    monkeypatch.setattr(notifier, "send", lambda msg: sent.setdefault("msg", msg))

    trade_data = {
        "Symbol": "ETHUSDT",
        "Side": "sell",
        "Price": 3000,
        "PositionSize": 0.5,
        "SL": 2900,
        "TP": 3200
    }
    notifier.trade_close(trade_data)
    assert "Закрыта сделка" in sent["msg"]
    assert "ETHUSDT" in sent["msg"]

def test_alert(monkeypatch):
    cfg = make_cfg()
    notifier = Notifier(cfg)
    sent = {}

    monkeypatch.setattr(notifier, "send", lambda msg: sent.setdefault("msg", msg))

    notifier.alert("Пробой уровня")
    assert "[ALERT]" in sent["msg"]
    assert "Пробой уровня" in sent["msg"]
