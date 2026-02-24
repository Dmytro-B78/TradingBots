# bot_ai/core/config_loader.py — Config: полноценный словарь через Mapping

import json
import os
from collections.abc import Mapping

class Config(Mapping):
    def __init__(self, path="config.json"):
        self.path = path
        self._load()

    def _load(self):
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Config file not found: {self.path}")
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._data = data

        # атрибуты для удобства
        self.risk = data.get("risk", {})
        self.sl_tp = data.get("sl_tp", {})
        self.notifications = data.get("notifications", {})
        self.strategy = data.get("strategy", {})
        self.pipeline = data.get("pipeline", {})

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return f"Config({self._data})"

    @staticmethod
    def load(path="config.json"):
        return Config(path)

