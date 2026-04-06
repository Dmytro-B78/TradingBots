# ================================================================
# File: bot_ai/engine/risk_manager.py
# NT-Tech RiskManager 1.2 (ASCII-only)
# Spot-only ATR-lazy risk engine
# ================================================================

class RiskManager:
    def __init__(self, config=None):
        # multipliers
        self.sl_mult = 1.5
        self.tp_mult = 2.0
        self.trailing_mult = 1.0

        # position state
        self.position = None
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.trailing_stop = None

        # risk control
        self.position_size = 1.0
        self.max_consecutive_losses = 5
        self.loss_streak = 0

        # ATR state
        self.atr_period = 14
        self.atr_values = []
        self.prev_close = None
    # ------------------------------------------------------------
    # ATR calculation
    # ------------------------------------------------------------
    def update_atr(self, candle):
        high = candle["high"]
        low = candle["low"]
        close = candle["close"]

        if self.prev_close is None:
            tr = high - low
        else:
            tr = max(
                high - low,
                abs(high - self.prev_close),
                abs(low - self.prev_close)
            )

        self.prev_close = close
        self.atr_values.append(tr)

        if len(self.atr_values) < self.atr_period:
            return None

        return sum(self.atr_values[-self.atr_period:]) / self.atr_period
    # ------------------------------------------------------------
    # Main handler
    # ------------------------------------------------------------
    def on_candle(self, candle, meta_signal):
        atr = self.update_atr(candle)
        price = candle["close"]

        # ATR not ready yet
        if atr is None:
            # allow opening a position without SL/TP
            if self.position is None:
                if meta_signal and meta_signal.get("signal") == "OPEN_LONG":
                    self.position = "LONG"
                    self.entry_price = price
                    self.stop_loss = None
                    self.take_profit = None
                    self.trailing_stop = None

                    return {
                        "action": "OPEN_LONG",
                        "price": price,
                        "position": self.position
                    }

            # if position is open but ATR not ready -> do nothing
            return None
        # initialize SL/TP/trailing once ATR becomes available
        if self.position == "LONG" and self.stop_loss is None:
            self.stop_loss = self.entry_price - atr * self.sl_mult
            self.take_profit = self.entry_price + atr * self.tp_mult
            self.trailing_stop = self.entry_price - atr * self.trailing_mult
        # --------------------------------------------------------
        # Manage LONG
        # --------------------------------------------------------
        if self.position == "LONG":

            # if SL/TP not initialized yet -> skip risk checks
            if self.stop_loss is None:
                return None

            # trailing update
            new_trail = price - atr * self.trailing_mult
            if new_trail > self.trailing_stop:
                self.trailing_stop = new_trail

            # stop loss
            if price <= self.stop_loss:
                self.position = None
                self.loss_streak += 1
                return {"action": "CLOSE_LONG_SL", "price": price}

            # trailing stop
            if price <= self.trailing_stop:
                self.position = None
                self.loss_streak = 0
                return {"action": "CLOSE_LONG_TRAIL", "price": price}

            # take profit
            if price >= self.take_profit:
                self.position = None
                self.loss_streak = 0
                return {"action": "CLOSE_LONG_TP", "price": price}

            # meta close
            if meta_signal and meta_signal.get("signal") == "CLOSE_LONG":
                self.position = None
                self.loss_streak = 0
                return {"action": "CLOSE_LONG_META", "price": price}
        # --------------------------------------------------------
        # Manage LONG
        # --------------------------------------------------------
        if self.position == "LONG":

            # if SL/TP not initialized yet -> skip risk checks
            if self.stop_loss is None:
                return None

            # trailing update
            new_trail = price - atr * self.trailing_mult
            if new_trail > self.trailing_stop:
                self.trailing_stop = new_trail

            # stop loss
            if price <= self.stop_loss:
                self.position = None
                self.loss_streak += 1
                return {"action": "CLOSE_LONG_SL", "price": price}

            # trailing stop
            if price <= self.trailing_stop:
                self.position = None
                self.loss_streak = 0
                return {"action": "CLOSE_LONG_TRAIL", "price": price}

            # take profit
            if price >= self.take_profit:
                self.position = None
                self.loss_streak = 0
                return {"action": "CLOSE_LONG_TP", "price": price}

            # meta close
            if meta_signal and meta_signal.get("signal") == "CLOSE_LONG":
                self.position = None
                self.loss_streak = 0
                return {"action": "CLOSE_LONG_META", "price": price}
        # halt trading after too many losses
        if self.loss_streak >= self.max_consecutive_losses:
            return {"action": "HALT_TRADING", "reason": "max_loss_streak"}

        return None
