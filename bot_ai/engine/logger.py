# ================================================================
# File: bot_ai/engine/logger.py
# Module: engine.logger
# Purpose: Lightweight NT-Tech logging utility
# Responsibilities:
#   - Provide simple console logging
#   - Format messages with levels
#   - Keep output minimal and readable
# Notes:
#   - ASCII-only
# ================================================================

import datetime


class Logger:
    """
    NT-Tech lightweight console logger.
    """

    # ------------------------------------------------------------
    # Timestamp in UTC
    # ------------------------------------------------------------
    @staticmethod
    def _ts():
        return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # ------------------------------------------------------------
    # Info level
    # ------------------------------------------------------------
    @staticmethod
    def info(msg):
        try:
            text = str(msg)
        except Exception:
            text = "<unprintable message>"
        print(f"[INFO] {Logger._ts()} | {text}")

    # ------------------------------------------------------------
    # Warning level
    # ------------------------------------------------------------
    @staticmethod
    def warn(msg):
        try:
            text = str(msg)
        except Exception:
            text = "<unprintable message>"
        print(f"[WARN] {Logger._ts()} | {text}")

    # ------------------------------------------------------------
    # Error level
    # ------------------------------------------------------------
    @staticmethod
    def error(msg):
        try:
            text = str(msg)
        except Exception:
            text = "<unprintable message>"
        print(f"[ERROR] {Logger._ts()} | {text}")
