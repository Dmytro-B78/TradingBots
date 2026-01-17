# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/state/position_store.py
# Назначение: Хранение и управление открытыми позициями
# ============================================

import os
import json
from datetime import datetime

class PositionStore:
    def __init__(self, path: str = "logs/positions.json"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2, ensure_ascii=False)

    def set(self, pair: str, signal: dict):
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)

        data[pair] = {
            "side": signal.get("side"),
            "entry": signal.get("entry"),
            "stop": signal.get("stop"),
            "target": signal.get("target"),
            "qty": signal.get("qty"),
            "timestamp": datetime.utcnow().isoformat()
        }

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get(self, pair: str) -> dict:
        if not os.path.exists(self.path):
            return {}
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(pair, {})

    def clear(self, pair: str):
        if not os.path.exists(self.path):
            return
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if pair in data:
            del data[pair]
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
