# ================================================================
# File: bot_ai/utils/logger.py
# Module: utils.logger
# Purpose: NT-Tech lightweight logging utility
# Responsibilities:
#   - Provide simple stdout logging
#   - Support info, warning, error levels
#   - Keep output clean and uniform
# Notes:
#   - ASCII-only
# ================================================================

import datetime


class Logger:
    """
    NT-Tech minimal logger.
    """

    @staticmethod
    def _ts():
        return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def info(msg):
        print(f"[INFO] {Logger._ts()} | {msg}")

    @staticmethod
    def warn(msg):
        print(f"[WARN] {Logger._ts()} | {msg}")

    @staticmethod
    def error(msg):
        print(f"[ERROR] {Logger._ts()} | {msg}")


log = Logger()
