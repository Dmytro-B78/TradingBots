import pytest
from bot_ai.execution.executor import TradeExecutor
from bot_ai.risk.position_sizer_sl import PositionSizerWithSL

@pytest.fixture
def dummy_executor():
    class DummyExecutor(TradeExecutor):
        def __init__(self):
            self.last_trade = None

        def execute_trade(self, pair, side, size, sl, tp):
            self.last_trade = {
                "pair": pair,
                "side": side,
                "size": size,
                "sl": sl,
                "tp": tp
            }

    return DummyExecutor()

def test_position_sizer_with_sl_basic(dummy_executor):
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {"risk_per_trade": 0.01})()
    cfg.sl_tp = type("SlTpCfg", (), {"sl_value": 2.0})()
    sizer = PositionSizerWithSL(cfg)

    balance = 1000
    price = 100
    sl = 2.0
    size = sizer.calculate_size(balance, price, sl)

    assert size == pytest.approx(5.0)

def test_position_sizer_with_sl_zero_sl(dummy_executor):
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {"risk_per_trade": 0.01})()
    cfg.sl_tp = type("SlTpCfg", (), {"sl_value": 0.0})()
    sizer = PositionSizerWithSL(cfg)

    balance = 1000
    price = 100
    sl = 0.0
    size = sizer.calculate_size(balance, price, sl)

    assert size == 0

