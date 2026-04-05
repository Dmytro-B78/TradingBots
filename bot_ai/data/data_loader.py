# ================================================================
# File: bot_ai/data/data_loader.py
# Module: data.data_loader
# Purpose: NT-Tech unified historical data loader
# Responsibilities:
#   - Load OHLC data from JSON or CSV
#   - Normalize candle structure
#   - Provide safe parsing utilities
# Notes:
#   - ASCII-only
# ================================================================

import json
import csv


class DataLoader:
    """
    NT-Tech data loader for OHLC candles.
    Supports JSON and CSV formats.
    """

    # ------------------------------------------------------------
    # JSON loader
    # ------------------------------------------------------------
    @staticmethod
    def load_json(path):
        with open(path, "r") as f:
            raw = json.load(f)

        candles = []
        for c in raw:
            candles.append({
                "time": c.get("time"),
                "open": float(c.get("open")),
                "high": float(c.get("high")),
                "low": float(c.get("low")),
                "close": float(c.get("close")),
                "volume": float(c.get("volume", 0))
            })

        return candles

    # ------------------------------------------------------------
    # CSV loader
    # ------------------------------------------------------------
    @staticmethod
    def load_csv(path):
        candles = []
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                candles.append({
                    "time": row.get("time"),
                    "open": float(row.get("open")),
                    "high": float(row.get("high")),
                    "low": float(row.get("low")),
                    "close": float(row.get("close")),
                    "volume": float(row.get("volume", 0))
                })
        return candles

    # ------------------------------------------------------------
    # Auto-detect loader
    # ------------------------------------------------------------
    @staticmethod
    def load(path):
        if path.lower().endswith(".json"):
            return DataLoader.load_json(path)
        if path.lower().endswith(".csv"):
            return DataLoader.load_csv(path)
        raise ValueError("Unsupported file format")
