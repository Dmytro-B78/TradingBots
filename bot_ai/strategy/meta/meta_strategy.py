# ================================================================
# File: C:\TradingBots\NT\bot_ai\strategy\meta\meta_strategy.py
# NT-Tech 2026 - MetaStrategy Core
# Stage1-Lite, Stage2-Lite v2, Re-Entry Engine,
# ATR-Trail 2.0 with Initial Wide Stop, new confidence model
# Integrated Stage 2.2: MetaSignalFilter (smoothing, hysteresis, 2-bar exit confirm)
# ASCII-only, deterministic
# ================================================================

from .stage1 import stage1_check
from .stage2 import stage2_check
from .entry_engine import compute_entry_signal
from .trail_engine import trail_engine
from .indicators import update_indicators
from .meta_signal_filter import MetaSignalFilter


class MetaStrategy:
    def __init__(self, params=None):
        # Position state
        self.position = None
        self.entry_price = None
        self.entry_bar_index = None
        self.max_price_since_entry = None

        self.last_exit_reason = None
        self.last_exit_bar_index = None

        self.open_condition_streak = 0
        self.required_streak = 1

        self.bar_index = 0

        # OHLC cache
        self.last_close = None
        self.last_open = None
        self.last_high = None
        self.last_low = None

        self.prev_close = None
        self.prev_open = None
        self.prev_high = None
        self.prev_low = None

        # EMA lengths (NT-Tech 2026 standard)
        self.ema_fast_len = 10
        self.ema_slow_len = 30
        self.ema_trend_len = 90

        # EMA values
        self.ema_fast = None
        self.prev_ema_fast = None
        self.ema_slow = None
        self.ema_trend = None

        # ATR settings
        self.atr_1h = None
        self.atr_4h = None
        self.atr_1h_mean = None
        self.atr_4h_mean = None
        self.atr_1h_alpha = 0.10
        self.atr_4h_alpha = 0.025

        # Derived indicators
        self.trend_strength = 0.0
        self.slope = 0.0
        self.momentum = 0.0

        # Histories
        self.momentum_hist = []
        self.slope_hist = []
        self.trend_hist = []

        # MTF bias
        self.mtf_bias_4h = 0.0

        # Regimes (needed by stage1/stage2/entry_engine)
        self.atr_regime_1h = "normal"
        self.atr_regime_4h = "normal"
        self.local_regime = "normal"
        self.global_regime = "normal"

        # Confidence (NT-Tech 2026 model)
        self.confidence = 0.0
        self._confidence_ema = None

        # Meta-signal filter (Stage 2.2)
        self.meta_filter = MetaSignalFilter()

    # ------------------------------------------------------------
    # Internal: update max price since entry
    # ------------------------------------------------------------
    def update_state(self, candle_close):
        if self.position == "LONG":
            if self.max_price_since_entry is None:
                self.max_price_since_entry = candle_close
            else:
                if candle_close > self.max_price_since_entry:
                    self.max_price_since_entry = candle_close

    # ------------------------------------------------------------
    # Compute ATR regimes and volatility regimes
    # ------------------------------------------------------------
    def _compute_regimes(self):
        atr_1h = self.atr_1h
        atr_4h = self.atr_4h
        atr_1h_mean = self.atr_1h_mean
        atr_4h_mean = self.atr_4h_mean

        atr_regime_1h = "normal"
        atr_regime_4h = "normal"

        if atr_1h is not None and atr_1h_mean is not None and atr_1h_mean > 0:
            ratio_1h = atr_1h / atr_1h_mean
            if ratio_1h > 1.5:
                atr_regime_1h = "high"
            elif ratio_1h < 0.75:
                atr_regime_1h = "low"

        if atr_4h is not None and atr_4h_mean is not None and atr_4h_mean > 0:
            ratio_4h = atr_4h / atr_4h_mean
            if ratio_4h > 1.5:
                atr_regime_4h = "high"
            elif ratio_4h < 0.75:
                atr_regime_4h = "low"

        local_regime = atr_regime_1h
        global_regime = atr_regime_4h

        # store on strategy for stage1/stage2/entry_engine
        self.atr_regime_1h = atr_regime_1h
        self.atr_regime_4h = atr_regime_4h
        self.local_regime = local_regime
        self.global_regime = global_regime

        return atr_regime_1h, atr_regime_4h, local_regime, global_regime

    # ------------------------------------------------------------
    # Compute confidence (NT-Tech 2026 model)
    # ------------------------------------------------------------
    def _update_confidence(self):
        ts = self.trend_strength if self.trend_strength is not None else 0.0
        sl = self.slope if self.slope is not None else 0.0
        mom = self.momentum if self.momentum is not None else 0.0

        confidence_raw = 0.4 * ts + 0.3 * sl + 0.3 * mom

        alpha = 0.20
        if self._confidence_ema is None:
            self._confidence_ema = confidence_raw
        else:
            self._confidence_ema = alpha * confidence_raw + (1.0 - alpha) * self._confidence_ema

        self.confidence = float(self._confidence_ema)

    # ------------------------------------------------------------
    # Build meta_state from current indicators and candle
    # ------------------------------------------------------------
    def compute_meta_state(self, candle):
        update_indicators(self, candle)

        close = float(candle["close"])
        high = float(candle["high"])
        low = float(candle["low"])
        open_price = float(candle.get("open", close))

        atr_regime_1h, atr_regime_4h, local_regime, global_regime = self._compute_regimes()

        self._update_confidence()

        meta_state = {
            "open": open_price,
            "high": high,
            "low": low,
            "close": close,
            "atr_1h": self.atr_1h,
            "atr_4h": self.atr_4h,
            "atr_regime_1h": atr_regime_1h,
            "atr_regime_4h": atr_regime_4h,
            "local_regime": local_regime,
            "global_regime": global_regime,
            "mtf_bias_4h": self.mtf_bias_4h,
            "momentum": self.momentum,
            "trend_strength": self.trend_strength,
            "slope": self.slope,
            "ema_fast": self.ema_fast,
            "confidence": self.confidence,
        }

        return meta_state

    # ------------------------------------------------------------
    # Entry logic
    # ------------------------------------------------------------
    def compute_entry(self, meta_state, debug_info):
        return compute_entry_signal(self, meta_state, debug_info)

    # ------------------------------------------------------------
    # Exit logic (ATR-Trail 2.0)
    # ------------------------------------------------------------
    def compute_exit(self, meta_state, debug_info):
        if self.position != "LONG":
            return None

        trail = trail_engine(self, meta_state)
        debug_info["trail"] = trail

        if trail is None:
            return None

        stop_price = trail["stop_price"]
        close = float(meta_state["close"])

        if close <= stop_price:
            self.position = None
            self.last_exit_reason = trail["kind"]
            self.last_exit_bar_index = self.bar_index

            return {
                "kind": "meta_signal",
                "signal": "CLOSE_LONG",
                "reason": trail["kind"],
                "exit_price": close,
                "confidence": float(meta_state["confidence"]),
            }

        return None

    # ------------------------------------------------------------
    # Legacy adapter for LiveEngine 4.3
    # With Stage 2.2 meta-signal filtering
    # ------------------------------------------------------------
    def compute_meta_signal(self, meta_state):
        debug_info = {}

        entry_decision = self.compute_entry(meta_state, debug_info)
        exit_decision = None
        if entry_decision is None:
            exit_decision = self.compute_exit(meta_state, debug_info)

        meta_signal = None
        exit_reason = None

        if entry_decision is not None:
            meta_signal = "OPEN_LONG"
        elif exit_decision is not None:
            meta_signal = "CLOSE_LONG"
            exit_reason = exit_decision.get("reason")

        if meta_signal is None:
            # still update filter state with no signal
            filter_result = self.meta_filter.process(
                meta_signal=None,
                raw_confidence=float(meta_state["confidence"]),
                exit_reason=None,
            )
            debug_info["meta_filter"] = filter_result
            return None

        filter_result = self.meta_filter.process(
            meta_signal=meta_signal,
            raw_confidence=float(meta_state["confidence"]),
            exit_reason=exit_reason,
        )
        debug_info["meta_filter"] = filter_result

        filtered_signal = filter_result["filtered_signal"]

        if filtered_signal is None:
            return None

        if filtered_signal == "OPEN_LONG" and entry_decision is not None:
            return entry_decision

        if filtered_signal == "CLOSE_LONG" and exit_decision is not None:
            return exit_decision

        return None

    # ------------------------------------------------------------
    # Main entry point for each bar (new architecture)
    # With Stage 2.2 meta-signal filtering
    # ------------------------------------------------------------
    def on_candle(self, candle):
        meta_state = self.compute_meta_state(candle)
        debug_info = {}

        self.bar_index += 1
        self.update_state(float(meta_state["close"]))

        entry_decision = self.compute_entry(meta_state, debug_info)
        exit_decision = None
        if entry_decision is None:
            exit_decision = self.compute_exit(meta_state, debug_info)

        meta_signal = None
        exit_reason = None

        if entry_decision is not None:
            meta_signal = "OPEN_LONG"
        elif exit_decision is not None:
            meta_signal = "CLOSE_LONG"
            exit_reason = exit_decision.get("reason")

        if meta_signal is None:
            filter_result = self.meta_filter.process(
                meta_signal=None,
                raw_confidence=float(meta_state["confidence"]),
                exit_reason=None,
            )
            debug_info["meta_filter"] = filter_result
            return None, debug_info

        filter_result = self.meta_filter.process(
            meta_signal=meta_signal,
            raw_confidence=float(meta_state["confidence"]),
            exit_reason=exit_reason,
        )
        debug_info["meta_filter"] = filter_result

        filtered_signal = filter_result["filtered_signal"]

        if filtered_signal is None:
            return None, debug_info

        if filtered_signal == "OPEN_LONG" and entry_decision is not None:
            return entry_decision, debug_info

        if filtered_signal == "CLOSE_LONG" and exit_decision is not None:
            return exit_decision, debug_info

        return None, debug_info
