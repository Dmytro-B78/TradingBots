# ============================================
# File: bot_ai/state/position_tracker.py
# Purpose: Persistent storage for open positions between sessions
# Format: UTF-8 without BOM
# ============================================

import json
import os

class PositionTracker:
    def __init__(self, symbol, timeframe, state_dir="bot_ai/state/positions"):
        self.symbol = symbol
        self.timeframe = timeframe
        self.state_dir = state_dir
        self.file_path = os.path.join(state_dir, f"{symbol}_{timeframe}_open_position.json")
        os.makedirs(self.state_dir, exist_ok=True)

    def save(self, time, price):
        data = {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "open_time": time,
            "open_price": price
        }
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self):
        if not os.path.exists(self.file_path):
            return None
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def clear(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
