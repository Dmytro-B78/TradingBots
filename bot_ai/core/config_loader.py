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
            if not isinstance(k, str):
                raise TypeError(f"Config.get(...) keys must be strings, got: {type(k)}")
            if not isinstance(cur, dict) or k not in cur:
                return default
            cur = cur[k]
        return cur

    def __getitem__(self, key: str) -> Any:
        return self.data.get(key)

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def __repr__(self):
        return f"<Config keys={list(self.data.keys())}>"
