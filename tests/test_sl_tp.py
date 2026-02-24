import pytest
import pandas as pd
from bot_ai.risk.sl_tp import SLTP

@pytest.fixture
def dummy_cfg():
    cfg = type("Cfg", (), {})()
    cfg.sl_tp = type("SlTpCfg", (), {
        "sl_type": "fixed",
        "sl_value": 2.0,
        "tp_value": 3.0
    })()
    return cfg

def test_sl_tp_fixed(dummy_cfg):
    sltp = SLTP(dummy_cfg)
    sl, tp = sltp.calculate(None, {"Price": 100, "Side": "buy"})
    assert sl == 98.0
    assert tp == 103.0

def test_sl_tp_fixed_sell(dummy_cfg):
    sltp = SLTP(dummy_cfg)
    sl, tp = sltp.calculate(None, {"Price": 100, "Side": "sell"})
    assert sl == 102.0
    assert tp == 97.0

