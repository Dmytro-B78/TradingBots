# ================================================================
# File: bot_ai/engine/data_loader.py
# NT-Tech DataLoader 3.1 (ASCII-only, deterministic)
# ================================================================

import os
import json
import csv


class DataLoader:
    """
    NT-Tech DataLoader 3.1
    Supports:
        - JSON files
        - CSV files (Binance kline format)
        - Directories containing mixed formats
    Produces:
        - Deterministic, sorted, unique OHLC candles
        - Unified format:
            {
                "open_time": int,
                "open": float,
                "high": float,
                "low": float,
                "close": float,
                "volume": float
            }
    """

    # ------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------
    @staticmethod
    def load(path):
        if os.path.isdir(path):
            return DataLoader._load_directory(path)
        if os.path.isfile(path):
            return DataLoader._load_file(path)
        raise Exception("Invalid path: not a file or directory")

    # ------------------------------------------------------------
    # Directory loader
    # ------------------------------------------------------------
    @staticmethod
    def _load_directory(dir_path):
        try:
            files = [
                os.path.join(dir_path, f)
                for f in os.listdir(dir_path)
                if f.lower().endswith(".json") or f.lower().endswith(".csv")
            ]
        except Exception:
            raise Exception("Failed to list directory")

        if not files:
            raise Exception("No JSON or CSV files found in directory")

        files.sort()
        rows = []

        for f in files:
            try:
                if f.lower().endswith(".json"):
                    rows.extend(DataLoader._read_json(f))
                elif f.lower().endswith(".csv"):
                    rows.extend(DataLoader._read_csv(f))
            except Exception:
                continue

        return DataLoader._normalize(rows)

    # ------------------------------------------------------------
    # Single file loader
    # ------------------------------------------------------------
    @staticmethod
    def _load_file(path):
        if path.lower().endswith(".json"):
            return DataLoader._normalize(DataLoader._read_json(path))
        if path.lower().endswith(".csv"):
            return DataLoader._normalize(DataLoader._read_csv(path))
        raise Exception("Unsupported file format (must be .json or .csv)")

    # ------------------------------------------------------------
    # JSON reader (ASCII-only)
    # ------------------------------------------------------------
    @staticmethod
    def _read_json(path):
        with open(path, "r", encoding="ascii", errors="ignore") as f:
            raw = json.load(f)
        if not isinstance(raw, list):
            raise Exception("JSON file must contain a list")
        return raw

    # ------------------------------------------------------------
    # CSV reader (Binance kline format)
    # ------------------------------------------------------------
    @staticmethod
    def _read_csv(path):
        rows = []
        with open(path, "r", encoding="ascii", errors="ignore") as f:
            reader = csv.reader(f)
            for parts in reader:
                # Binance kline has 12 fields, but we only need first 6
                if len(parts) < 6:
                    continue
                try:
                    row = [
                        int(parts[0]),      # open_time
                        float(parts[1]),    # open
                        float(parts[2]),    # high
                        float(parts[3]),    # low
                        float(parts[4]),    # close
                        float(parts[5])     # volume
                    ]
                    rows.append(row)
                except Exception:
                    continue
        return rows

    # ------------------------------------------------------------
    # Normalize Binance kline format into OHLC dicts
    # ------------------------------------------------------------
    @staticmethod
    def _normalize(raw):
        if not isinstance(raw, list):
            raise Exception("Invalid candle data format: expected list")

        candles = []
        seen = set()

        for row in raw:
            if not isinstance(row, list) or len(row) < 6:
                continue

            try:
                open_time = int(row[0])
                if open_time in seen:
                    continue
                seen.add(open_time)

                candle = {
                    "open_time": open_time,
                    "open": float(row[1]),
                    "high": float(row[2]),
                    "low": float(row[3]),
                    "close": float(row[4]),
                    "volume": float(row[5])
                }

                candles.append(candle)

            except Exception:
                continue

        candles.sort(key=lambda x: x["open_time"])
        return candles
