import pytest
import requests
from types import SimpleNamespace
from bot_ai.utils.notifier import Notifier

def make_cfg(enabled=True, provider="telegram", token="T", chat_id="C"):
    return SimpleNamespace(
        notifications=SimpleNamespace(
            enabled=enabled,
            provider=provider,
            telegram_token=token,
            telegram_chat_id=chat_id
        )
    )

def test_send_success(monkeypatch):
    cfg = make_cfg()
    notifier = Notifier(cfg)
    called = {}
    def fake_post(url, data, timeout):
        called["url"] = url
        called["data"] = data
        class Resp:
            status_code = 200
            text = "OK"
        return Resp()
    monkeypatch.setattr(requests, "post", fake_post)
    notifier.send("hello")
    assert called["data"]["text"] == "hello"

def test_send_empty_disabled(monkeypatch):
    cfg = make_cfg(enabled=False)
    notifier = Notifier(cfg)
    called = {"flag": False}
    def mark_called(*a, **k):
        called["flag"] = True
    monkeypatch.setattr(requests, "post", mark_called)
    notifier.send("should not send")
    assert called["flag"] is False

def test_send_network_error(monkeypatch):
    cfg = make_cfg()
    notifier = Notifier(cfg)
    def fail(*a, **k):
        raise ConnectionError("network down")
    monkeypatch.setattr(requests, "post", fail)
    notifier.send("test message")

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
    assert "Открыта позиция" in sent["msg"]

def test_trade_close(monkeypatch):
    cfg = make_cfg()
    notifier = Notifier(cfg)
    sent = {}
    monkeypatch.setattr(notifier, "send", lambda msg: sent.setdefault("msg", msg))
    trade_data = {
        "Symbol": "BTCUSDT",
        "Side": "sell",
        "Price": 51000,
        "Profit(%)": 5,
        "Profit(USDT)": 250
    }
    notifier.trade_close(trade_data)
    assert "Закрыта позиция" in sent["msg"]

def test_alert(monkeypatch):
    cfg = make_cfg()
    notifier = Notifier(cfg)
    sent = {}
    monkeypatch.setattr(notifier, "send", lambda msg: sent.setdefault("msg", msg))
    notifier.alert("Test alert")
    assert "АЛЕРТ" in sent["msg"]
