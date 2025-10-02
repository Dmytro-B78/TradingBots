import pytest
from bot_ai.risk.sl_tp import DynamicSLTP

@pytest.mark.parametrize("atr,volatility,min_stop,max_stop", [
    (0.5, 0.01, 0.2, 5.0),
    (1.0, 0.05, 0.2, 5.0),
    (2.0, 0.10, 0.2, 5.0),
])
def test_dynamic_sltp_bounds(atr, volatility, min_stop, max_stop):
    """
    Проверка, что SL находится в пределах min_stop и max_stop,
    а TP всегда положительный.
    """
    sltp = DynamicSLTP(min_stop=min_stop, max_stop=max_stop)
    sl, tp = sltp.calculate(atr=atr, volatility=volatility)
    assert min_stop <= sl <= max_stop, f"SL {sl} вне допустимых границ"
    assert tp > 0, "TP должен быть положительным"
