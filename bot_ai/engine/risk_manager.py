# ================================================================
# File: bot_ai/engine/risk_manager.py
# NT-Tech Institutional PositionManager 3.3-TS6V2
# - Smooth trailing (TS6)
# - Volatility-adaptive trailing (Vol Guard, safe)
# - trailing_mult default = 0.6
# - ASCII-only, deterministic
# ================================================================

from bot_ai.execution.risk_engine import RiskEngine as CoreRiskEngine


class RiskManager:
    def __init__(self, config=None):
        config = config or {}

        self.risk = CoreRiskEngine(config.get("risk_engine", {}))
        self.enable_kill_switch = bool(config.get("enable_kill_switch", False))

        self.position = None
        self.entry_price = None
        self.size = 0.0
        self.notional = 0.0
        self.stop_price = None
        self.trailing_stop = None

        self.realized_pnl = 0.0

        # Base trailing multiplier
        self.trailing_mult = float(config.get("trailing_mult", 0.6))

        # Volatility thresholds
        self.low_vol_threshold = float(config.get("low_vol_threshold", 0.9))
        self.high_vol_threshold = float(config.get("high_vol_threshold", 1.4))

    # ------------------------------------------------------------
    def _debug(self, msg, ctx=None):
        print("RISK_DEBUG:", msg, ctx or {})

    # ------------------------------------------------------------
    def update_equity(self, equity):
        self.risk.update_equity(equity)

    # ------------------------------------------------------------
    def _reset_position(self):
        self.position = None
        self.entry_price = None
        self.size = 0.0
        self.notional = 0.0
        self.stop_price = None
        self.trailing_stop = None

    # ------------------------------------------------------------
    def _close_position(self, price, reason, meta_state=None, confidence=None):
        if self.position != "LONG" or self.size <= 0 or self.entry_price is None:
            self._debug("close_called_without_position")
            self._reset_position()
            return {"action": "NO_POSITION", "reason": "close_called_without_position"}

        pnl = (price - self.entry_price) * self.size
        self.realized_pnl += pnl

        self.risk.register_realized_pnl(pnl)
        self.risk.register_close_exposure(self.notional)

        resp = {
            "action": "CLOSE_LONG",
            "reason": reason,
            "price": price,
            "pnl": pnl
        }

        meta_state = meta_state or {}
        if confidence is not None:
            resp["confidence"] = confidence

        resp.update({
            "atr_1h": meta_state.get("atr_1h"),
            "atr_4h": meta_state.get("atr_4h"),
            "atr_regime_1h": meta_state.get("atr_regime_1h"),
            "atr_regime_4h": meta_state.get("atr_regime_4h"),
            "local_regime": meta_state.get("local_regime"),
            "global_regime": meta_state.get("global_regime"),
            "mtf_bias_4h": meta_state.get("mtf_bias_4h"),
        })

        self._debug("CLOSE_POSITION", resp)
        self._reset_position()
        return resp

    # ------------------------------------------------------------
    def on_candle(self, candle, meta_signal, meta_state=None):
        price = candle.get("close")
        if price is None or price <= 0:
            self._debug("invalid_price", {"price": price})
            return None

        meta_state = meta_state or {}
        signal = meta_signal.get("signal") if meta_signal else None
        confidence = meta_signal.get("confidence") if meta_signal else None

        # Kill switch
        if self.enable_kill_switch and self.risk.is_kill_switch_active():
            self._debug("kill_switch_active")
            return {"action": "HALT_TRADING", "reason": "kill_switch_active"}

        # --------------------------------------------------------
        # OPEN LOGIC
        # --------------------------------------------------------
        if self.position is None:
            if signal != "OPEN_LONG":
                return None

            atr_1h = meta_state.get("atr_1h")
            atr_4h = meta_state.get("atr_4h")
            atr_regime_1h = meta_state.get("atr_regime_1h")
            atr_regime_4h = meta_state.get("atr_regime_4h")
            local_regime = meta_state.get("local_regime")
            global_regime = meta_state.get("global_regime")
            mtf_bias_4h = meta_state.get("mtf_bias_4h")

            if atr_1h is None or atr_1h <= 0:
                self._debug("skip_open", {"reason": "atr_1h_not_ready"})
                return {"action": "SKIP_OPEN", "reason": "atr_1h_not_ready"}

            order = self.risk.compute_order(
                side="LONG",
                price=price,
                atr_1h=atr_1h,
                atr_4h=atr_4h,
                atr_regime_1h=atr_regime_1h,
                atr_regime_4h=atr_regime_4h,
                local_regime=local_regime,
                global_regime=global_regime,
                mtf_bias_4h=mtf_bias_4h,
                confidence=confidence
            )

            if not order or order.get("reason") != "ok" or order.get("size", 0.0) <= 0:
                self._debug("risk_engine_block", order or {"reason": "risk_engine_none"})
                return {"action": "SKIP_OPEN", "reason": order.get("reason", "risk_engine_blocked")}

            # OPEN POSITION
            self.position = "LONG"
            self.entry_price = price
            self.size = float(order["size"])
            self.notional = float(order["notional"])
            self.stop_price = float(order["stop_price"])

            self.risk.register_open_exposure(self.notional)

            if self.trailing_mult > 0 and atr_1h is not None:
                self.trailing_stop = price - atr_1h * self.trailing_mult
            else:
                self.trailing_stop = None

            resp = {
                "action": "OPEN_LONG",
                "side": "BUY",
                "size": self.size,
                "price": price,
                "stop_price": self.stop_price,
                "trailing_stop": self.trailing_stop,
                "risk": {
                    "risk_pct": order.get("risk_pct"),
                    "kill_switch": order.get("kill_switch", False)
                }
            }

            if confidence is not None:
                resp["confidence"] = confidence

            resp.update({
                "atr_1h": atr_1h,
                "atr_4h": atr_4h,
                "atr_regime_1h": atr_regime_1h,
                "atr_regime_4h": atr_regime_4h,
                "local_regime": local_regime,
                "global_regime": global_regime,
                "mtf_bias_4h": mtf_bias_4h,
            })

            self._debug("OPEN_LONG", resp)
            return resp

        # --------------------------------------------------------
        # POSITION MANAGEMENT (LONG)
        # --------------------------------------------------------
        if self.position == "LONG":
            atr_1h = meta_state.get("atr_1h")
            atr_4h = meta_state.get("atr_4h")
            atr_regime_1h = meta_state.get("atr_regime_1h")
            atr_regime_4h = meta_state.get("atr_regime_4h")
            local_regime = meta_state.get("local_regime")
            global_regime = meta_state.get("global_regime")
            mtf_bias_4h = meta_state.get("mtf_bias_4h")

            # Dynamic stop refinement
            if atr_1h is not None and atr_1h > 0:
                order = self.risk.compute_order(
                    side="LONG",
                    price=price,
                    atr_1h=atr_1h,
                    atr_4h=atr_4h,
                    atr_regime_1h=atr_regime_1h,
                    atr_regime_4h=atr_regime_4h,
                    local_regime=local_regime,
                    global_regime=global_regime,
                    mtf_bias_4h=mtf_bias_4h,
                    confidence=confidence
                )
                if order and order.get("reason") == "ok":
                    new_stop_price = float(order["stop_price"])
                    if self.stop_price is None or new_stop_price > self.stop_price:
                        self._debug("tighten_stop", {"old": self.stop_price, "new": new_stop_price})
                        self.stop_price = new_stop_price

            # --------------------------------------------------------
            # Volatility-Adaptive Smooth Trailing (TS6V2)
            # --------------------------------------------------------
            if self.trailing_mult > 0 and atr_1h is not None:
                # Safe ATR mean from meta_state
                atr_mean = meta_state.get("atr_1h_mean") or atr_1h
                vol_factor = atr_1h / atr_mean

                # Adjust trailing multiplier
                if vol_factor > self.high_vol_threshold:
                    adj_mult = self.trailing_mult * 1.25
                elif vol_factor < self.low_vol_threshold:
                    adj_mult = self.trailing_mult * 0.85
                else:
                    adj_mult = self.trailing_mult

                raw_trail = price - atr_1h * adj_mult

                if self.trailing_stop is None:
                    self.trailing_stop = raw_trail
                else:
                    max_step = atr_1h * 0.3
                    allowed_trail = self.trailing_stop + max_step
                    new_trail = min(raw_trail, allowed_trail)

                    if new_trail > self.trailing_stop:
                        self._debug("trail_update_vol_smooth", {
                            "old": self.trailing_stop,
                            "raw": raw_trail,
                            "limited": new_trail,
                            "vol_factor": vol_factor,
                            "adj_mult": adj_mult,
                            "max_step": max_step
                        })
                        self.trailing_stop = new_trail

            # Ensure trailing_stop >= stop_price
            if self.stop_price is not None and self.trailing_stop is not None:
                if self.trailing_stop < self.stop_price:
                    self.trailing_stop = self.stop_price

            # Hard stop
            if self.stop_price is not None and price <= self.stop_price:
                self._debug("HARD_STOP", {"price": price, "stop": self.stop_price})
                return self._close_position(price, "STOP_LOSS", meta_state, confidence)

            # Trailing stop
            if self.trailing_stop is not None and price <= self.trailing_stop:
                self._debug("TRAILING_STOP", {"price": price, "trail": self.trailing_stop})
                return self._close_position(price, "TRAILING_STOP", meta_state, confidence)

            # Meta close
            if signal == "CLOSE_LONG":
                self._debug("META_CLOSE", {"price": price})
                return self._close_position(price, "META_CLOSE", meta_state, confidence)

        return None
