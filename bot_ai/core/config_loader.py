import json
from pathlib import Path
from typing import Any, Dict

class Config:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @classmethod
    def load(cls, path: str = "config.json") -> "Config":
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Config not found: {path}")
        with p.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)
        return cls(data)

    def get(self, *keys, default=None):
        cur = self.data
        for k in keys:
            if not isinstance(cur, dict) or k not in cur:
                return default
            cur = cur[k]
        return cur