# ================================================================
# File: bot_ai/strategy/meta/meta_signal_filter.py
# NT-Tech MetaSignal Filter - Stage 2.2
# - meta_signal smoothing
# - 2-bar exit confirmation
# - confidence hysteresis
# ASCII-only
# ================================================================

from typing import Dict, Any, Optional


class MetaSignalFilter:
    """
    Stateful filter for meta_signal:
      - smooths confidence
      - applies hysteresis for OPEN/CLOSE
      - enforces N-bar confirmation for exits
    """

    def __init__(
        self,
        smooth_alpha: float = 0.35,
        open_conf_low: float = 0.05,
        open_conf_high: float = 0.08,
        close_conf_low: float = 0.03,
        close_conf_high: float = 0.06,
        exit_confirm_bars: int = 2,
    ) -> None:
        self.smooth_alpha = smooth_alpha
        self.smoothed_conf: Optional[float] = None

        self.open_conf_low = open_conf_low
        self.open_conf_high = open_conf_high
        self.close_conf_low = close_conf_low
        self.close_conf_high = close_conf_high

        self.exit_confirm_bars = exit_confirm_bars
        self._pending_exit_reason: Optional[str] = None
        self._pending_exit_count: int = 0

        self.in_position: bool = False

    # ------------------------------------------------------------
    # Confidence smoothing (EMA)
    # ------------------------------------------------------------
    def _smooth_confidence(self, raw_conf: float) -> float:
        if self.smoothed_conf is None:
            self.smoothed_conf = raw_conf
        else:
            a = self.smooth_alpha
            self.smoothed_conf = a * raw_conf + (1.0 - a) * self.smoothed_conf
        return self.smoothed_conf

    # ------------------------------------------------------------
    # Hysteresis for open
    # ------------------------------------------------------------
    def _allow_open(self, conf: float) -> bool:
        if not self.in_position:
            return conf >= self.open_conf_high
        return conf >= self.open_conf_low

    # ------------------------------------------------------------
    # Hysteresis for close
    # ------------------------------------------------------------
    def _allow_close(self, conf: float) -> bool:
        if not self.in_position:
            return False
        return conf <= self.close_conf_low

    # ------------------------------------------------------------
    # Exit confirmation (N-bar)
    # ------------------------------------------------------------
    def _process_exit_confirmation(self, exit_reason: str, allow_now: bool) -> bool:
        if not allow_now:
            self._pending_exit_reason = None
            self._pending_exit_count = 0
            return False

        if self._pending_exit_reason is None:
            self._pending_exit_reason = exit_reason
            self._pending_exit_count = 1
            return False

        if self._pending_exit_reason != exit_reason:
            self._pending_exit_reason = exit_reason
            self._pending_exit_count = 1
            return False

        self._pending_exit_count += 1
        if self._pending_exit_count >= self.exit_confirm_bars:
            self._pending_exit_reason = None
            self._pending_exit_count = 0
            return True

        return False

    # ------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------
    def process(
        self,
        meta_signal: Optional[str],
        raw_confidence: float,
        exit_reason: Optional[str],
    ) -> Dict[str, Any]:
        sm_conf = self._smooth_confidence(raw_confidence)

        filtered_signal: Optional[str] = None
        exit_confirmed = False

        if meta_signal == "OPEN_LONG":
            if self._allow_open(sm_conf):
                filtered_signal = "OPEN_LONG"
                self.in_position = True

        elif meta_signal == "CLOSE_LONG" and exit_reason is not None:
            allow_close_now = self._allow_close(sm_conf)
            if self.in_position:
                if self._process_exit_confirmation(exit_reason, allow_close_now):
                    filtered_signal = "CLOSE_LONG"
                    exit_confirmed = True
                    self.in_position = False

        return {
            "filtered_signal": filtered_signal,
            "smoothed_confidence": sm_conf,
            "exit_confirmed": exit_confirmed,
        }
