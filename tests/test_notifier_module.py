import logging
from types import SimpleNamespace

def test_notifier_all_branches(monkeypatch, caplog):
    """
    Полный тест всех веток Notifier:
    - отключённые уведомления
    - отправка в Telegram (успех, ошибка, исключение)
    - отправка в консоль
    - методы trade_open, trade_close, alert
    """
    from bot_ai.utils.notifier import Notifier

    caplog.set_level(logging.INFO)

    # 1. enabled=False > send ничего не делает
    cfg_disabled = SimpleNamespace(
        notifications=SimpleNamespace(
            enabled=False))
    n_disabled = Notifier(cfg_disabled)
    assert n_disabled.enabled is False
    n_disabled.send("msg")  # ничего не логируется

    # 2. enabled=True, provider=telegram, успешный POST
    cfg_enabled = SimpleNamespace(
        notifications=SimpleNamespace(
            enabled=True,
            provider="telegram",
            telegram_token="token",
            telegram_chat_id="chat"))
    n_enabled = Notifier(cfg_enabled)
    monkeypatch.setattr("bot_ai.utils.notifier.requests.post",
                        lambda *a, **k: type("Resp", (), {"status_code": 200})())
    n_enabled.send("test message")

    # 3. POST возвращает код ? 200
    monkeypatch.setattr("bot_ai.utils.notifier.requests.post", lambda *a,
                        **k: type("Resp", (), {"status_code": 500, "text": "fail"})())
    caplog.clear()
    n_enabled.send("bad message")
    assert any("Ошибка отправки" in m for m in caplog.messages)

    # 4. Исключение при POST
    def raise_exc(*a, **k): raise ConnectionError("fail")
    monkeypatch.setattr("bot_ai.utils.notifier.requests.post", raise_exc)
    caplog.clear()
    n_enabled.send("exception message")
    assert any("Ошибка при отправке" in m for m in caplog.messages)

    # 5. provider?telegram > логируется [NOTIFY]
    cfg_other = SimpleNamespace(
        notifications=SimpleNamespace(
            enabled=True, provider="console"))
    n_other = Notifier(cfg_other)
    caplog.clear()
    n_other.send("console message")
    assert any("[NOTIFY]" in m for m in caplog.messages)

    # 6. trade_open / trade_close / alert — проверяем через свой список
    sent_msgs = []
    monkeypatch.setattr(n_other, "send", lambda msg: sent_msgs.append(msg))
    trade_data = {
        "Symbol": "BTCUSDT",
        "Side": "buy",
        "Price": 100,
        "PositionSize": 1,
        "SL": 90,
        "TP": 110,
        "Profit(%)": 5,
        "Profit(USDT)": 10
    }
    n_other.trade_open(trade_data)
    n_other.trade_close(trade_data)
    n_other.alert("Warning")
    assert any("Открыта позиция" in m for m in sent_msgs)
    assert any("Закрыта позиция" in m for m in sent_msgs)
    assert any("АЛЕРТ" in m for m in sent_msgs)

