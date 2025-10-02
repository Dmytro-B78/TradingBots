import pytest
from types import SimpleNamespace
from bot_ai.signals import sl_tp

def make_cfg(sl_type="atr", sl_value=2.0, tp_type="r_multiple", tp_value=3.0):
    return SimpleNamespace(
        sl_tp=SimpleNamespace(
            sl_type=sl_type,
            sl_value=sl_value,
            tp_type=tp_type,
            tp_value=tp_value
        )
    )

def test_sl_tp_standard_long():
    cfg = make_cfg()
    result = sl_tp.calculate_sl_tp(entry_price=100, side="long", cfg=cfg, atr_value=5)
    assert result["sl_price"] == 90.0
    assert result["tp_price"] == 130.0

def test_sl_tp_standard_short():
    cfg = make_cfg()
    result = sl_tp.calculate_sl_tp(entry_price=100, side="short", cfg=cfg, atr_value=5)
    assert result["sl_price"] == 110.0
    assert result["tp_price"] == 70.0

def test_sl_tp_fixed():
    cfg = make_cfg(sl_type="fixed", sl_value=10, tp_type="fixed", tp_value=20)
    result = sl_tp.calculate_sl_tp(entry_price=100, side="long", cfg=cfg, atr_value=5)
    assert result["sl_price"] == 90.0
    assert result["tp_price"] == 120.0

def test_sl_tp_invalid_sl_type():
    cfg = make_cfg(sl_type="unknown")
    with pytest.raises(ValueError):
        sl_tp.calculate_sl_tp(entry_price=100, side="long", cfg=cfg, atr_value=5)

def test_sl_tp_invalid_tp_type():
    cfg = make_cfg(tp_type="unknown")
    with pytest.raises(ValueError):
        sl_tp.calculate_sl_tp(entry_price=100, side="long", cfg=cfg, atr_value=5)

def test_sl_tp_invalid_side():
    cfg = make_cfg()
    with pytest.raises(ValueError):
        sl_tp.calculate_sl_tp(entry_price=100, side="invalid", cfg=cfg, atr_value=5)
