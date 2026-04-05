# ================================================================
# File: bot_ai/engine/config_loader.py
# NT-Tech ConfigLoader 3.0 (Strict Mode C compatible)
# ASCII-only
# ================================================================

import json


class ConfigLoader:
    """
    NT-Tech configuration loader.
    Supports:
        - allow_live_trading (Strict Mode C master switch)
        - dry_run (script override allowed)
        - meta_strategy block
        - strategy parameter blocks (ma_crossover, rsi, macd, bollinger, etc.)
    """

    @staticmethod
    def load_from_json(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return ConfigLoader._normalize(data)
        except Exception as e:
            raise Exception("Failed to load config JSON: " + str(e))

    @staticmethod
    def load_from_dict(data):
        return ConfigLoader._normalize(data)

    @staticmethod
    def _normalize(data):
        if not isinstance(data, dict):
            raise Exception("Config must be a dictionary")

        # ------------------------------------------------------------
        # allow_live_trading (Strict Mode C)
        # ------------------------------------------------------------
        allow_live_trading = bool(data.get("allow_live_trading", False))

        # ------------------------------------------------------------
        # dry_run (can be overridden by scripts)
        # ------------------------------------------------------------
        dry_run = bool(data.get("dry_run", True))

        # ------------------------------------------------------------
        # meta_strategy block
        # ------------------------------------------------------------
        meta = data.get("meta_strategy", None)
        if not isinstance(meta, dict):
            raise Exception("Config missing required block: meta_strategy")

        # ------------------------------------------------------------
        # Strategy parameter blocks
        # ------------------------------------------------------------
        strategies = {}
        for key, value in data.items():
            if key in ["allow_live_trading", "dry_run", "meta_strategy"]:
                continue
            if isinstance(value, dict):
                strategies[key] = value

        if not strategies:
            raise Exception("No strategy parameter blocks found in config")

        # ------------------------------------------------------------
        # Final normalized config
        # ------------------------------------------------------------
        return {
            "allow_live_trading": allow_live_trading,
            "dry_run": dry_run,
            "meta_strategy": meta,
            "strategies": strategies
        }
