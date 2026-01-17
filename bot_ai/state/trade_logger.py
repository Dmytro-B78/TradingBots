# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/state/trade_logger.py
# Назначение: Логирование сделок по всем режимам
# ============================================

import os
import json
from datetime import datetime

class TradeLogger:
    def __init__(self, path: str = "logs/trades.json"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2, ensure_ascii=False)

    def log(self, signal: dict, pair: str, timeframe: str, mode: str):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "pair": pair,
            "timeframe": timeframe,
            "mode": mode,
            "side": signal.get("side"),
            "entry": signal.get("entry"),
            "stop": signal.get("stop"),
            "target": signal.get("target"),
            "qty": signal.get("qty")
        }

        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)

        data.append(entry)

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
