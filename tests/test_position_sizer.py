import logging
import pytest

def test_position_sizer_calculate_size_all_branches(caplog):
    from bot_ai.risk.position_sizer import PositionSizer

    # Базовая конфигурация
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {
        "test_equity": 1000,
        "risk_per_trade_pct": 1.0,
        "leverage": 1.0,
        "min_size_usdt": 10.0,
        "max_size_usdt": 100000.0,
        "position_notional_usdt": None
    })()

    ps = PositionSizer(cfg)

    # 1. Со стопом, нормальная дистанция
    size1 = ps.calculate_size(entry_price=100, stop_price=90)
    assert size1 > 0

    # 2. Со стопом, дистанция <= 0
    caplog.set_level(logging.WARNING)
    size2 = ps.calculate_size(entry_price=100, stop_price=100)
    assert size2 > 0
    assert any("Stop distance <= 0" in m for m in caplog.messages)

    # 3. Без стопа, фиксированный нотионал
    cfg.risk.position_notional_usdt = 500
    size3 = ps.calculate_size(entry_price=100)
    assert size3 == 500

    # 4. Без стопа, без фиксированного — расчёт от капитала
    cfg.risk.position_notional_usdt = None
    size4 = ps.calculate_size(entry_price=100)
    assert size4 > 0

    # 5. Ограничение min_usdt
    cfg.risk.test_equity = 1
    cfg.risk.risk_per_trade_pct = 0.0001
    size5 = ps.calculate_size(entry_price=100)
    assert size5 == cfg.risk.min_size_usdt

    # 6. Ограничение max_usdt
    cfg.risk.test_equity = 1_000_000
    cfg.risk.risk_per_trade_pct = 100
    size6 = ps.calculate_size(entry_price=100)
    assert size6 == cfg.risk.max_size_usdt
