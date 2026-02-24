"""
Модуль динамического расчёта SL/TP на основе конфигурации.
"""

import logging

class DynamicSLTP:
    def __init__(self, cfg):
        self.cfg = cfg
        self.logger = logging.getLogger(__name__)

    def apply(self, df):
        if not self.cfg.get("enabled", False):
            self.logger.info("Dynamic SLTP отключён")
            return df

        sl_mult = self.cfg.get("sl_multiplier", 0.02)
        tp_mult = self.cfg.get("tp_multiplier", 0.04)

        def compute_sl(row):
            price = row["entry_price"]
            if row["side"] == "long":
                return price * (1 - sl_mult)
            else:
                return price * (1 + sl_mult)

        def compute_tp(row):
            price = row["entry_price"]
            if row["side"] == "long":
                return price * (1 + tp_mult)
            else:
                return price * (1 - tp_mult)

        df["sl"] = df.apply(compute_sl, axis=1)
        df["tp"] = df.apply(compute_tp, axis=1)
        return df
