# ================================================================
# NT-Tech 2026 - MetaStrategy 9.0 (Thin Orchestrator)
# File: bot_ai/strategy/meta/meta_strategy.py
# ASCII-only, deterministic, no Cyrillic
# ================================================================

from .indicators import update_indicators
from .regimes import update_regimes
from .stage1 import stage1_check
from .stage2 import stage2_check
from .exits import (
    exit_profit_lock,
    exit_soft,
    compute_dynamic_rr,
    smooth_soft_exit,
    modulate_soft_exit_raw,
)
from .intrabar_stops import (
    intrabar_abs_stop,
    intrabar_hwm_stop,
    intrabar_atr_trail,
    intrabar_ema_stop,
    adjust_trailing_mult_by_regime,
)
from ..filters import apply_meta_filters
from .extended_logger import ExtendedMetaLogger


class MetaStrategy:
    def __init__(self, config=None):
        config = config or {}

        # --------------------------------------------------------
        # Core parameters
        # --------------------------------------------------------
        self.ema_fast_len = int(config.get("ema_fast_len", 30))
        self.ema_slow_len = int(config.get("ema_slow_len", 90))
        self.ema_trend_len = int(config.get("ema_trend_len", 180))

        self.atr_1h_alpha = float(config.get("atr_1h_alpha", 2.0 / 30.0))
        self.atr_4h_alpha = float(config.get("atr_4h_alpha", 2.0 / 120.0))

        self.ema_conf_alpha = float(config.get("ema_conf_alpha", 0.06))

        # Aggression factor
        self.aggression_factor = float(config.get("aggression_factor", 0.45))

        # Stage thresholds (scaled)
        self.s1_min_conf = float(config.get("s1_min_conf", 0.03)) * self.aggression_factor
        self.s1_min_trend = float(config.get("s1_min_trend", 0.03)) * self.aggression_factor
        self.s1_min_slope = float(config.get("s1_min_slope", 0.010)) * self.aggression_factor
        self.s1_min_momentum = float(config.get("s1_min_momentum", 0.010)) * self.aggression_factor

        self.s2_min_conf = float(config.get("s2_min_conf", 0.08)) * self.aggression_factor
        self.s2_min_trend = float(config.get("s2_min_trend", 0.06)) * self.aggression_factor
        self.s2_min_slope = float(config.get("s2_min_slope", 0.018)) * self.aggression_factor
        self.s2_min_momentum = float(config.get("s2_min_momentum", 0.035)) * self.aggression_factor
        self.s2_min_mtf_bias_4h = float(config.get("s2_min_mtf_bias_4h", 0.05)) * self.aggression_factor

        self.impulse_window = int(config.get("impulse_window", 2))

        # Exit parameters
        self.momentum_exit_threshold = float(config.get("momentum_exit_threshold", -0.05))
        self.atr_profit_lock_rr = float(config.get("atr_profit_lock_rr", 1.5))
        self.ema_fast_stop_mult = float(config.get("ema_fast_stop_mult", 1.0))
        self.close_thr = float(config.get("close_thr", 0.05))

        self.abs_loss_stop_pct = float(config.get("abs_loss_stop_pct", -0.06))
        self.hwm_drawdown_stop_pct = float(config.get("hwm_drawdown_stop_pct", -0.06))
        self.atr_trail_mult = float(config.get("atr_trail_mult", 1.2))

        # Soft-exit smoothing
        self.soft_exit_alpha = 0.25
        self.soft_exit_ema = None

        # Entry streak
        self.open_condition_streak = 0
        self.required_streak = int(config.get("required_streak", 1))

        # --------------------------------------------------------
        # State
        # --------------------------------------------------------
        self.position = None
        self.entry_price = None
        self.entry_bar_index = None
        self.bar_index = 0
        self.max_price_since_entry = None

        self.last_open = None
        self.last_high = None
        self.last_low = None
        self.last_close = None

        self.prev_open = None
        self.prev_high = None
        self.prev_low = None
        self.prev_close = None

        self.prev_ema_fast = None

        self.ema_fast = None
        self.ema_slow = None
        self.ema_trend = None

        self.atr_1h = None
        self.atr_4h = None
        self.atr_1h_mean = None
        self.atr_4h_mean = None

        self.local_regime = None
        self.global_regime = None
        self.atr_regime_1h = None
        self.atr_regime_4h = None
        self.mtf_bias_4h = 0.0

        self.trend_strength = 0.0
        self.slope = 0.0
        self.momentum = 0.0

        self.momentum_hist = []
        self.slope_hist = []
        self.trend_hist = []

        self.ema_conf = None

        self.logger = ExtendedMetaLogger()

    # ------------------------------------------------------------
    def _compute_raw_confidence(self):
        regime_score = 0.05 if self.global_regime == "trend" else -0.05 if self.global_regime == "expansion" else 0.0
        raw = (
            0.5 * self.trend_strength +
            0.3 * self.slope +
            0.2 * self.momentum +
            regime_score
        )
        return max(min(raw, 1.0), -1.0)

    # ------------------------------------------------------------
    def compute_meta_state(self, candle):
        update_indicators(self, candle)
        update_regimes(self)

        raw_conf = self._compute_raw_confidence()
        self.ema_conf = (
            raw_conf if self.ema_conf is None
            else self.ema_conf_alpha * raw_conf + (1.0 - self.ema_conf_alpha) * self.ema_conf
        )
        smooth_conf = max(min(self.ema_conf, 1.0), -1.0)

        return {
            "confidence": smooth_conf,
            "atr_1h": self.atr_1h,
            "atr_4h": self.atr_4h,
            "atr_regime_1h": self.atr_regime_1h,
            "atr_regime_4h": self.atr_regime_4h,
            "local_regime": self.local_regime,
            "global_regime": self.global_regime,
            "mtf_bias_4h": self.mtf_bias_4h,
            "momentum": self.momentum,
            "trend_strength": self.trend_strength,
            "slope": self.slope,
            "ema_fast": self.ema_fast,
            "close": self.last_close,
            "low": self.last_low,
        }

    # ------------------------------------------------------------
    def compute_meta_signal(self, s):
        debug_info = {}

        smooth_conf = float(s["confidence"])
        local_regime = s["local_regime"]
        global_regime = s["global_regime"]
        atr_regime_1h = s["atr_regime_1h"]

        momentum = float(s["momentum"])
        trend_strength = float(s["trend_strength"])
        slope = float(s["slope"])
        close = float(s["close"])
        low = float(s["low"])

        # --------------------------------------------------------
        # Entry filters
        # --------------------------------------------------------
        f = apply_meta_filters({
            "atr_1h_entry": s["atr_1h"],
            "confidence_entry": smooth_conf,
            "local_regime": local_regime,
            "global_regime": global_regime,
        })
        debug_info["filters"] = f.__dict__

        if not f.passed:
            self.logger.log({"close": close}, s, debug_info, None)
            return None

        # --------------------------------------------------------
        # ENTRY LOGIC
        # --------------------------------------------------------
        if self.position is None:
            s1_ok = stage1_check(self, smooth_conf, local_regime)
            s2_ok = stage2_check(self, smooth_conf, local_regime)

            debug_info["stage1"] = s1_ok
            debug_info["stage2"] = s2_ok

            if s1_ok and s2_ok:
                self.open_condition_streak += 1
            else:
                self.open_condition_streak = 0

            if self.open_condition_streak >= self.required_streak:
                self.position = "LONG"
                self.entry_price = close
                self.entry_bar_index = self.bar_index
                self.max_price_since_entry = close
                self.open_condition_streak = 0

                decision = {"kind": "meta_signal", "signal": "OPEN_LONG", "confidence": smooth_conf}
                self.logger.log({"close": close}, s, debug_info, decision)
                return decision

            self.logger.log({"close": close}, s, debug_info, None)
            return None

        # --------------------------------------------------------
        # EXIT LOGIC
        # --------------------------------------------------------
        if self.position == "LONG":
            exit_reason = None
            exit_price = close

            # ATR-Regime trailing modulation
            self.atr_trail_mult = adjust_trailing_mult_by_regime(
                self.atr_trail_mult,
                local_regime
            )

            # Intrabar stops
            for stop_fn in [
                intrabar_abs_stop,
                intrabar_hwm_stop,
                intrabar_atr_trail,
                intrabar_ema_stop,
            ]:
                rp = stop_fn(self, low)
                if rp is not None:
                    exit_reason, exit_price = rp
                    debug_info["intrabar_stop"] = stop_fn.__name__
                    break

            # Profit lock (dynamic + ATR-aware)
            if exit_reason is None:
                dyn_rr = compute_dynamic_rr(
                    trend_strength,
                    slope,
                    momentum,
                    self.atr_profit_lock_rr,
                    local_regime
                )

                base_rr = self.atr_profit_lock_rr
                self.atr_profit_lock_rr = dyn_rr

                r = exit_profit_lock(self, close)
                self.atr_profit_lock_rr = base_rr

                if r is not None:
                    exit_reason = r
                    debug_info["profit_lock_rr"] = dyn_rr

            # Soft exit (smoothed + ATR-aware)
            if exit_reason is None:
                raw_soft = 1.0 if exit_soft(
                    self,
                    smooth_conf,
                    s["mtf_bias_4h"],
                    atr_regime_1h,
                    momentum,
                    trend_strength,
                    local_regime,
                ) is not None else 0.0

                raw_soft = modulate_soft_exit_raw(raw_soft, local_regime)
                smooth_soft = smooth_soft_exit(self.soft_exit_ema, raw_soft, self.soft_exit_alpha)
                self.soft_exit_ema = smooth_soft

                debug_info["soft_exit_raw"] = raw_soft
                debug_info["soft_exit_smooth"] = smooth_soft

                if smooth_soft > 0.6:
                    exit_reason = "SOFT_EXIT_SMOOTH"

            # Finalize exit
            if exit_reason:
                self.position = None
                self.entry_price = None
                self.entry_bar_index = None
                self.max_price_since_entry = None
                self.open_condition_streak = 0

                decision = {
                    "kind": "meta_signal",
                    "signal": "CLOSE_LONG",
                    "reason": exit_reason,
                    "exit_price": exit_price,
                    "confidence": smooth_conf,
                }
                self.logger.log({"close": close}, s, debug_info, decision)
                return decision

            self.logger.log({"close": close}, s, debug_info, None)
            return None

        return None
