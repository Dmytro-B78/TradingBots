# bot_ai/risk/sl_tp_OLD.py
# ------------------------------------------------------------
# Назначение:
# Модуль для расчёта динамических уровней Stop Loss (SL) и Take Profit (TP)
# на основе ATR (Average True Range) и показателя волатильности.
# ------------------------------------------------------------

from dataclasses import dataclass

@dataclass
class DynamicSLTP:
    """
    Класс для расчёта динамических SL и TP.
    min_stop — минимальный допустимый стоп (в пунктах или %)
    max_stop — максимальный допустимый стоп (в пунктах или %)
    """
    min_stop: float
    max_stop: float

    def calculate(self, atr: float, volatility: float):
        """
        Расчёт SL и TP:
        - SL = ATR * (1 + volatility)
        - Ограничение SL в пределах [min_stop, max_stop]
        - TP = SL * коэффициент прибыли (по умолчанию 2.0)
        """
        # Базовый расчёт стопа
        sl = atr * (1 + volatility)

        # Ограничиваем стоп в допустимых пределах
        if sl < self.min_stop:
            sl = self.min_stop
        elif sl > self.max_stop:
            sl = self.max_stop

        # Take Profit — в 2 раза больше стопа
        tp = sl * 2.0

        return sl, tp

