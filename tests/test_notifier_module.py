import logging
import pytest
from types import SimpleNamespace
from bot_ai.utils.notifier import Notifier

def test_notifier_all_branches(monkeypatch, caplog):
    """
    Проверяет все ветки поведения Notifier:
    - отключённые уведомления
    - отправка через Telegram (успех, ошибка, исключение)
    - отправка через console
    - методы trade_open, trade_close, alert
    """
    caplog.set_level(logging.INFO)

    # 1. Уведомления отключены
    cfg_disabled = SimpleNamespace(notifications=SimpleNamespace(enabled=False))
    n_disabled = Notifier(cfg_disabled)
    assert not n_disabled.enabled
    n_disabled.send("message")  # ничего не должно произойти

    # 2. Уведомления включены, Telegram: успешный POST
    cfg_enabled = SimpleNamespace(
        notifications=SimpleNamespace(
            enabled=True,
            provider="telegram",
            telegram_token="token",
            telegram_chat_id="chat"
        )
    )
    n_enabled = Notifier(cfg_enabled)
    monkeypatch.setattr("bot_ai.utils.notifier.requests.post",
                        lambda *a, **k: type("Resp", (), {"status_code": 200})())
    n_enabled.send("test message")

    # 3. Telegram: неудачный POST (500)
    monkeypatch.setattr("bot_ai.utils.notifier.requests.post",
                        lambda *a, **k: type("Resp", (), {"status_code": 500, "text": "fail"})())
    caplog.clear()
    n_enabled.send("bad message")
    assert any("Ошибка отправки уведомления" in m for m in caplog.messages)

    # 4. Telegram: исключение при POST
    def raise_exc(*a, **k): raise ConnectionError("fail")
    monkeypatch.setattr("bot_ai.utils.notifier.requests.post", raise_exc)
    caplog.clear()
    n_enabled.send("exception message")
    assert any("Ошибка отправки уведомления" in m for m in caplog.messages)

    # 5. Провайдер console
    cfg_console = SimpleNamespace(notifications=SimpleNamespace(enabled=True, provider="console"))
    n_console = Notifier(cfg_console)
    caplog.clear()
    n_console.send("console message")
    assert any("[NOTIFY]" in m for m in caplog.messages)

    # 6. Методы trade_open, trade_close, alert
    sent = []
    monkeypatch.setattr(n_console, "send", lambda msg: sent.append(msg))
    trade = {
        "Symbol": "BTCUSDT",
        "Side": "buy",
        "Price": 100,
        "PositionSize": 1,
        "SL": 90,
        "TP": 110,
        "Profit(%)": 5,
        "Profit(USDT)": 10
    }
    n_console.trade_open(trade)
    n_console.trade_close(trade)
    n_console.alert("Warning")
    assert any("BTCUSDT" in m for m in sent)
    assert any("Warning" in m for m in sent)
