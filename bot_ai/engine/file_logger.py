# ================================================================
# File: bot_ai/engine/file_logger.py
# NT-Tech FileLogger 3.0 (ASCII-only, deterministic)
# ================================================================

import os
import datetime


class FileLogger:
    LOG_DIR = "C:/TradingBots/NT/logs"
    LOG_FILE = "live_log.txt"
    MAX_BACKUPS = 5
    MAX_SIZE_MB = 5

    # ------------------------------------------------------------
    # Ensure log directory exists
    # ------------------------------------------------------------
    @staticmethod
    def _ensure_dir():
        try:
            if not os.path.exists(FileLogger.LOG_DIR):
                os.makedirs(FileLogger.LOG_DIR)
        except Exception:
            pass

    # ------------------------------------------------------------
    # Full path to active log file
    # ------------------------------------------------------------
    @staticmethod
    def _path():
        return os.path.join(FileLogger.LOG_DIR, FileLogger.LOG_FILE)

    # ------------------------------------------------------------
    # Timestamp in UTC
    # ------------------------------------------------------------
    @staticmethod
    def _timestamp():
        return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # ------------------------------------------------------------
    # Rotate log if size exceeds limit
    # ------------------------------------------------------------
    @staticmethod
    def _rotate_if_needed():
        path = FileLogger._path()

        if not os.path.exists(path):
            return

        try:
            size = os.path.getsize(path)
        except Exception:
            return

        max_size = FileLogger.MAX_SIZE_MB * 1024 * 1024

        if size < max_size:
            return

        ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        rotated = f"{path}.{ts}.bak"

        try:
            os.rename(path, rotated)
        except Exception:
            return

        FileLogger._cleanup_backups()

    # ------------------------------------------------------------
    # Remove old backups beyond MAX_BACKUPS
    # ------------------------------------------------------------
    @staticmethod
    def _cleanup_backups():
        try:
            files = [
                f for f in os.listdir(FileLogger.LOG_DIR)
                if f.startswith(FileLogger.LOG_FILE) and f.endswith(".bak")
            ]
            files.sort(reverse=True)

            for old in files[FileLogger.MAX_BACKUPS:]:
                try:
                    os.remove(os.path.join(FileLogger.LOG_DIR, old))
                except Exception:
                    pass
        except Exception:
            pass

    # ------------------------------------------------------------
    # Write log entry (ASCII-only)
    # ------------------------------------------------------------
    @staticmethod
    def write(level, message):
        FileLogger._ensure_dir()
        FileLogger._rotate_if_needed()

        try:
            msg = str(message)
        except Exception:
            msg = "<unprintable>"

        # enforce ASCII-only
        msg = msg.encode("ascii", errors="ignore").decode("ascii")

        line = f"[{level}] {FileLogger._timestamp()} | {msg}\n"

        try:
            with open(FileLogger._path(), "a", encoding="ascii", errors="ignore") as f:
                f.write(line)
        except Exception:
            pass

    # ------------------------------------------------------------
    # Convenience wrappers
    # ------------------------------------------------------------
    @staticmethod
    def info(msg):
        FileLogger.write("INFO", msg)

    @staticmethod
    def warn(msg):
        FileLogger.write("WARN", msg)

    @staticmethod
    def error(msg):
        FileLogger.write("ERROR", msg)
