# ================================================================
# File: bot_ai/strategy/meta/extended_logger.py
# NT-Tech 2026 - Extended Meta Logger (JSONL)
# ASCII-only, deterministic, no Cyrillic
# ================================================================

import os
import json
import datetime


class ExtendedMetaLogger:
    def __init__(self):
        # Create directory
        base_dir = os.path.join("C:\\TradingBots\\NT", "logs", "strategies")
        os.makedirs(base_dir, exist_ok=True)

        # File name
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = os.path.join(base_dir, f"meta_log_{ts}.jsonl")

        # Open file
        self.f = open(self.log_path, "a", encoding="utf-8")

    # ------------------------------------------------------------
    def log(self, candle, state, debug_info, decision):
        """
        Writes one JSONL record per bar.
        """

        record = {
            "bar_index": state.get("bar_index"),
            "timestamp": datetime.datetime.utcnow().isoformat(),

            # Candle
            "candle": {
                "open": candle.get("open"),
                "high": candle.get("high"),
                "low": candle.get("low"),
                "close": candle.get("close"),
            },

            # State
            "state": {
                "confidence": state.get("confidence"),
                "atr_1h": state.get("atr_1h"),
                "atr_4h": state.get("atr_4h"),
                "atr_regime_1h": state.get("atr_regime_1h"),
                "atr_regime_4h": state.get("atr_regime_4h"),
                "local_regime": state.get("local_regime"),
                "global_regime": state.get("global_regime"),
                "mtf_bias_4h": state.get("mtf_bias_4h"),
                "momentum": state.get("momentum"),
                "trend_strength": state.get("trend_strength"),
                "slope": state.get("slope"),
                "ema_fast": state.get("ema_fast"),
            },

            # Debug info (filters, stage1, stage2, soft_exit, etc.)
            "debug": debug_info,

            # Decision (open/close)
            "decision": decision,
        }

        self.f.write(json.dumps(record) + "\n")
        self.f.flush()

    # ------------------------------------------------------------
    def close(self):
        try:
            self.f.close()
        except:
            pass
