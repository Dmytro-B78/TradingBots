# ============================================
# File: C:\TradingBots\NT\bot_ai\risk\cooldown.py
# Purpose: Simple cooldown tracker for tests
# Encoding: UTF-8 without BOM
# ============================================

import json
import os
import time

class Cooldown:
    def __init__(self, path="cooldown.json", cooldown_hours=24):
        self.path = path
        self.cooldown_seconds = cooldown_hours * 3600
        self.data = {}

        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {}

    def is_blocked(self, pair):
        ts = self.data.get(pair)
        if not ts:
            return False
        return (time.time() - ts) < self.cooldown_seconds

    def update(self, pair):
        self.data[pair] = time.time()
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception:
            pass
