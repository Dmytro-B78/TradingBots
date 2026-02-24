# ============================================
# File: bot_ai/strategy/volume_spike_strategy.py
# Purpose: Volume spike strategy detecting abnormal volume surges
# Format: UTF-8 without BOM
# Compatible with: Signal, config, logging
# ============================================

import pandas as pd
import logging
from bot_ai.core.signal import Signal

class VolumeSpikeStrategy:
    def __init__(self, config: dict):
        self.volume_window = config.get("volume_window", 20)
        self.volume_multiplier = config.get("volume_multiplier", 2.0)

    def generate_signal(self, df: pd.DataFrame) -> Signal | None:
        if df is None or df.empty or len(df) < self.volume_window + 1:
            logging.debug(f"[SKIP] VolumeSpike | insufficient candles (len={len(df)})")
            return None

        df = df.copy()
        recent = df["volume"].iloc[-self.volume_window - 1:-1]
        current = df.iloc[-1]
        symbol = current.get("symbol", "UNKNOWN")

        avg_volume = recent.mean()
        threshold = avg_volume * self.volume_multiplier
        current_volume = current["volume"]

        logging.debug(f"[DEBUG] VolumeSpike | current_volume={current_volume:.2f} avg_volume={avg_volume:.2f} threshold={threshold:.2f}")

        if current_volume > threshold:
            signal = Signal("buy", symbol, df.index[-1],
                            entry_price=round(current["close"], 8),
                            strategy_name="volume_spike")
            logging.info(f"[SIGNAL] {signal}")
            return signal

        logging.debug(f"[SKIP] VolumeSpike | volume {current_volume:.2f} below threshold {threshold:.2f}")
        return None
