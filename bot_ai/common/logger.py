# ================================================================
# File: bot_ai/common/logger.py
# Module: common.logger
# Purpose: NT-Tech logging utilities
# Responsibilities:
#   - Provide unified logging interface
#   - Format logs consistently across modules
#   - Support debug/info/warning/error levels
# Notes:
#   - ASCII-only
# ================================================================

import datetime

class Logger:
    def __init__(self, name="NT-Tech"):
        self.name = name

    def _log(self, level, message):
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{self.name}] [{level}] {message}")

    def info(self, message):
        self._log("INFO", message)

    def debug(self, message):
        self._log("DEBUG", message)

    def warning(self, message):
        self._log("WARNING", message)

    def error(self, message):
        self._log("ERROR", message)
