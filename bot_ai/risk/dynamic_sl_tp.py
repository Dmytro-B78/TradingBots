import pandas as pd
import logging

class DynamicSLTP:
    def __init__(self, cfg):
        self.cfg = cfg
        self.logger = logging.getLogger(__name__)

        # Читаем параметры из risk, при отсутствии — из sl_tp, при отсутствии — дефолт
        self.sl_mult = getattr(cfg.risk, "sl_atr_multiplier",
                               getattr(cfg.sl_tp, "sl_value", 2.0))
        self.tp_mult = getattr(cfg.risk, "tp_atr_multiplier",
                               getattr(cfg.sl_tp, "tp_value", 3.0))
        self.atr_period = getattr(cfg.risk, "atr_period", 14)

    def _calculate_atr(self, df: pd.DataFrame):
        """
        Рассчитывает ATR по DataFrame с колонками: high, low, close
        """
        try:
            high = df["high"]
            low = df["low"]
            close = df["close"]
            tr1 = high - low
            tr2 = (high - close.shift()).abs()
            tr3 = (low - close.shift()).abs()
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(window=self.atr_period, min_periods=1).mean()
            return atr.iloc[-1]
        except Exception as e:
            self.logger.error(f"Ошибка расчёта ATR: {e}")
            return None

    def calculate(self, ohlcv_df: pd.DataFrame, trade_data: dict):
        """
        Возвращает (SL, TP) для сделки на основе ATR.
        """
        if ohlcv_df is None or ohlcv_df.empty:
            self.logger.warning("DynamicSLTP: нет данных OHLCV для расчёта SL/TP.")
            return None, None

        atr_value = self._calculate_atr(ohlcv_df)
        if atr_value is None or atr_value <= 0:
            self.logger.warning("DynamicSLTP: ATR не рассчитан или <= 0.")
            return None, None

        entry_price = trade_data.get("Price")
        side = trade_data.get("Side", "").lower()

        if not entry_price:
            self.logger.warning("DynamicSLTP: нет цены входа для расчёта SL/TP.")
            return None, None

        if side == "buy":
            sl = round(entry_price - atr_value * self.sl_mult, 6)
            tp = round(entry_price + atr_value * self.tp_mult, 6)
        elif side == "sell":
            sl = round(entry_price + atr_value * self.sl_mult, 6)
            tp = round(entry_price - atr_value * self.tp_mult, 6)
        else:
            self.logger.warning(f"DynamicSLTP: неизвестная сторона сделки {side}")
            return None, None

        self.logger.info(f"DynamicSLTP: ATR={atr_value:.6f}, SL={sl}, TP={tp}")
        return sl, tp
