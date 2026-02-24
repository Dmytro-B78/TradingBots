# ============================================
# File: C:\TradingBots\NT\bot_ai\strategy\volume_spike.py
# Purpose: Volume spike strategy class definition (fixed: added self to method)
# Encoding: UTF-8 without BOM
# ============================================

import pandas as pd
from bot_ai.strategy.base_strategy import BaseStrategy

class VolumeSpikeStrategy(BaseStrategy):
    def generate_signal(self, df: pd.DataFrame, params: dict):
        volume_window = params.get("volume_window", 20)
        spike_multiplier = params.get("spike_multiplier", 2.0)

        avg_volume = df["volume"].rolling(volume_window).mean()
        current_volume = df["volume"].iloc[-1]

        if current_volume > spike_multiplier * avg_volume.iloc[-1]:
            if df["close"].iloc[-1] > df["open"].iloc[-1]:
                return self.create_signal("buy", df)
            elif df["close"].iloc[-1] < df["open"].iloc[-1]:
                return self.create_signal("sell", df)
        return None
