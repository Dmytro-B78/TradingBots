import logging

class PositionSizer:
    """
    Рассчитывает размер позиции с учётом процента риска и стоп-дистанции.
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.logger = logging.getLogger(__name__)

    def calculate_size(
            self,
            entry_price: float,
            stop_price: float = None) -> float:
        try:
            risk_cfg = getattr(self.cfg, "risk", self.cfg)

            test_equity = getattr(
                risk_cfg,
                "test_equity",
                1000) if hasattr(
                risk_cfg,
                "__dict__") else risk_cfg.get(
                "test_equity",
                1000)
            risk_pct = getattr(
                risk_cfg,
                "risk_per_trade_pct",
                1.0) if hasattr(
                risk_cfg,
                "__dict__") else risk_cfg.get(
                "risk_per_trade_pct",
                1.0)
            leverage = getattr(
                risk_cfg,
                "leverage",
                1.0) if hasattr(
                risk_cfg,
                "__dict__") else risk_cfg.get(
                "leverage",
                1.0)
            min_usdt = getattr(
                risk_cfg,
                "min_size_usdt",
                10.0) if hasattr(
                risk_cfg,
                "__dict__") else risk_cfg.get(
                "min_size_usdt",
                10.0)
            max_usdt = getattr(
                risk_cfg,
                "max_size_usdt",
                100000.0) if hasattr(
                risk_cfg,
                "__dict__") else risk_cfg.get(
                "max_size_usdt",
                100000.0)
            fixed_notional = getattr(
                risk_cfg, "position_notional_usdt", None) or (
                risk_cfg.get("position_notional_usdt") if isinstance(
                    risk_cfg, dict) else None)

            # Если передан стоп — всегда считаем от стопа
            if stop_price is not None:
                risk_amount = test_equity * (risk_pct / 100.0)
                stop_distance = abs(entry_price - stop_price)
                if stop_distance <= 0:
                    self.logger.warning(
                        "Stop distance <= 0, fallback на фиксированный нотионал")
                    notional = risk_amount * leverage
                else:
                    qty = risk_amount / stop_distance
                    notional = qty * entry_price * leverage
            else:
                # Если стопа нет — используем фиксированный нотионал или риск
                # от капитала
                if fixed_notional is not None:
                    notional = float(fixed_notional)
                else:
                    risk_amount = test_equity * (risk_pct / 100.0)
                    notional = risk_amount * leverage

            # Ограничения
            notional = max(min_usdt, min(notional, max_usdt))

            return round(float(notional), 2)
        except Exception as e:
            self.logger.error(f"Ошибка в PositionSizer.calculate_size: {e}")
            return 0.0

