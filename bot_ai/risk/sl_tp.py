import pandas as pd

class SLTP:
    def __init__(self, config):
        self.config = config

    def calculate(self, df, context):
        price = context.get("Price")
        side = context.get("Side")
        sl_value = self.config.sl_tp.sl_value
        tp_value = self.config.sl_tp.tp_value

        if price is None or side not in ("buy", "sell"):
            return None, None

        if side == "buy":
            sl = price - sl_value
            tp = price + tp_value
        else:
            sl = price + sl_value
            tp = price - tp_value

        return sl, tp

class DynamicSLTP:
    def __init__(self, config):
        self.config = config

    def calculate(self, df, context):
        import logging
        price = context.get("Price")
        side = context.get("Side")

        if df is None or df.empty:
            logging.warning("Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћ Р В Р’В Р вЂ™Р’В Р В РЎС›Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РІР‚вЂњР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р вЂ™Р’В¦ OHLCV")
            return None, None

        high = df["high"]
        low = df["low"]
        close = df["close"]

        atr = (high - low).rolling(self.config.risk.atr_period).mean()
        atr_value = atr.iloc[-1] if not atr.isna().all() else 0

        if atr_value <= 0:
            logging.warning("ATR <= 0")
            return None, None

        if price is None or side not in ("buy", "sell"):
            return None, None

        sl_offset = atr_value * self.config.risk.sl_atr_multiplier
        tp_offset = atr_value * self.config.risk.tp_atr_multiplier

        if side == "buy":
            sl = price - sl_offset
            tp = price + tp_offset
        else:
            sl = price + sl_offset
            tp = price - tp_offset

        return sl, tp

