# ================================================================
# File: bot_ai/execution/risk_engine.py
# NT-Tech Institutional Risk Engine 3.0-AS-KS-RP-RS
# - Thin orchestrator
# - Uses risk_policy.py for logic
# - Uses risk_state.py for state
# ASCII-only, deterministic
# ================================================================

from bot_ai.execution.risk_policy import (
    compute_risk_pct,
    compute_stop_mult,
    compute_sizing_factors,
)
from bot_ai.execution.risk_state import RiskState


class RiskEngine:
    """
    Thin orchestrator:
      - delegates state to RiskState
      - delegates logic to risk_policy
      - builds final order dict
    """

    def __init__(self, config=None):
        config = config or {}

        # Policy parameters
        self.base_risk_pct = float(config.get("base_risk_pct", 0.0075))
        self.max_risk_pct = float(config.get("max_risk_pct", 0.015))
        self.min_risk_pct = float(config.get("min_risk_pct", 0.0025))

        self.stop_mult_base = float(config.get("stop_mult_base", 1.8))
        self.stop_mult_low_vol = float(config.get("stop_mult_low_vol", 1.4))
        self.stop_mult_high_vol = float(config.get("stop_mult_high_vol", 2.2))
        self.stop_mult_extreme_vol = float(config.get("stop_mult_extreme_vol", 2.8))

        self.atr_ratio_shock = float(config.get("atr_ratio_shock", 2.5))
        self.shock_risk_scale = float(config.get("shock_risk_scale", 0.5))

        self.trend_risk_boost = float(config.get("trend_risk_boost", 1.1))
        self.range_risk_scale = float(config.get("range_risk_scale", 0.8))
        self.compression_risk_scale = float(config.get("compression_risk_scale", 0.6))
        self.expansion_risk_scale = float(config.get("expansion_risk_scale", 1.0))

        self.max_exposure_pct = float(config.get("max_exposure_pct", 0.30))

        # State container
        self.state = RiskState(
            initial_equity=float(config.get("initial_equity", 10000.0)),
            max_daily_loss_pct=float(config.get("max_daily_loss_pct", 0.03)),
            max_weekly_loss_pct=float(config.get("max_weekly_loss_pct", 0.07)),
            max_losing_streak=int(config.get("max_losing_streak", 4)),
            streak_loss_pct=float(config.get("streak_loss_pct", 0.03)),
        )

        self.ignore_kill_switch = bool(config.get("ignore_kill_switch", False))

    # ------------------------------------------------------------
    # State passthrough
    # ------------------------------------------------------------

    def update_equity(self, equity):
        self.state.update_equity(equity)

    def register_realized_pnl(self, pnl):
        self.state.register_realized_pnl(pnl)

    def register_open_exposure(self, notional):
        self.state.register_open_exposure(notional)

    def register_close_exposure(self, notional):
        self.state.register_close_exposure(notional)

    def is_kill_switch_active(self):
        return self.state.is_kill_switch_active()

    def reset_kill_switch(self):
        self.state.reset_kill_switch()

    # ------------------------------------------------------------
    # Core order computation
    # ------------------------------------------------------------

    def compute_order(
        self,
        side,
        price,
        atr_1h,
        atr_4h,
        atr_regime_1h,
        atr_regime_4h,
        local_regime,
        global_regime,
        mtf_bias_4h,
        confidence=None,
    ):
        print("RISKENGINE_30_ACTIVE")

        if self.state.kill_switch_active and not self.ignore_kill_switch:
            return {
                "side": side,
                "size": 0.0,
                "notional": 0.0,
                "stop_price": None,
                "stop_distance": 0.0,
                "risk_pct": 0.0,
                "kill_switch": True,
                "reason": "kill_switch_active",
            }

        if side != "LONG":
            return {
                "side": side,
                "size": 0.0,
                "notional": 0.0,
                "stop_price": None,
                "stop_distance": 0.0,
                "risk_pct": 0.0,
                "kill_switch": self.state.kill_switch_active,
                "reason": "unsupported_side",
            }

        if price <= 0 or atr_1h is None or atr_1h <= 0:
            return {
                "side": side,
                "size": 0.0,
                "notional": 0.0,
                "stop_price": None,
                "stop_distance": 0.0,
                "risk_pct": 0.0,
                "kill_switch": self.state.kill_switch_active,
                "reason": "invalid_price_or_atr",
            }

        risk_pct, atr_ratio = compute_risk_pct(
            base_risk_pct=self.base_risk_pct,
            max_risk_pct=self.max_risk_pct,
            min_risk_pct=self.min_risk_pct,
            atr_1h=atr_1h,
            atr_4h=atr_4h,
            atr_regime_1h=atr_regime_1h,
            atr_regime_4h=atr_regime_4h,
            local_regime=local_regime,
            global_regime=global_regime,
            mtf_bias_4h=mtf_bias_4h,
            confidence=confidence,
            atr_ratio_shock=self.atr_ratio_shock,
            shock_risk_scale=self.shock_risk_scale,
            trend_risk_boost=self.trend_risk_boost,
            range_risk_scale=self.range_risk_scale,
            compression_risk_scale=self.compression_risk_scale,
            expansion_risk_scale=self.expansion_risk_scale,
        )

        stop_mult = compute_stop_mult(
            stop_mult_base=self.stop_mult_base,
            stop_mult_low_vol=self.stop_mult_low_vol,
            stop_mult_high_vol=self.stop_mult_high_vol,
            stop_mult_extreme_vol=self.stop_mult_extreme_vol,
            atr_regime_1h=atr_regime_1h,
            atr_regime_4h=atr_regime_4h,
            global_regime=global_regime,
            mtf_bias_4h=mtf_bias_4h,
            atr_ratio=atr_ratio,
            confidence=confidence,
        )

        stop_distance = atr_1h * stop_mult
        if stop_distance <= 0 or stop_distance >= price * 0.9:
            return {
                "side": side,
                "size": 0.0,
                "notional": 0.0,
                "stop_price": None,
                "stop_distance": 0.0,
                "risk_pct": 0.0,
                "kill_switch": self.state.kill_switch_active,
                "reason": "invalid_stop_distance",
            }

        stop_price = price - stop_distance

        risk_amount = self.state.equity * risk_pct
        if risk_amount <= 0:
            return {
                "side": side,
                "size": 0.0,
                "notional": 0.0,
                "stop_price": None,
                "stop_distance": 0.0,
                "risk_pct": 0.0,
                "kill_switch": self.state.kill_switch_active,
                "reason": "non_positive_risk_amount",
            }

        position_size = risk_amount / stop_distance

        atr_factor, conf_scale, regime_factor = compute_sizing_factors(
            price=price,
            atr_1h=atr_1h,
            local_regime=local_regime,
            confidence=confidence,
        )

        position_size *= atr_factor
        position_size *= conf_scale
        position_size *= regime_factor

        notional = position_size * price

        max_exposure = self.state.equity * self.max_exposure_pct
        if self.state.open_exposure + notional > max_exposure:
            available = max_exposure - self.state.open_exposure
            if available <= 0:
                return {
                    "side": side,
                    "size": 0.0,
                    "notional": 0.0,
                    "stop_price": None,
                    "stop_distance": 0.0,
                    "risk_pct": 0.0,
                    "kill_switch": self.state.kill_switch_active,
                    "reason": "max_exposure_reached",
                }
            scale = available / notional
            position_size *= scale
            notional = position_size * price

        if position_size <= 0:
            return {
                "side": side,
                "size": 0.0,
                "notional": 0.0,
                "stop_price": None,
                "stop_distance": 0.0,
                "risk_pct": 0.0,
                "kill_switch": self.state.kill_switch_active,
                "reason": "non_positive_position_size",
            }

        return {
            "side": side,
            "size": position_size,
            "notional": notional,
            "stop_price": stop_price,
            "stop_distance": stop_distance,
            "risk_pct": risk_pct,
            "kill_switch": self.state.kill_switch_active,
            "reason": "ok",
        }
