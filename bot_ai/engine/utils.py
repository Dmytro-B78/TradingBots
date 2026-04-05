# ================================================================
# File: bot_ai/engine/utils.py
# NT-Tech Utils 3.0 (ASCII-only, deterministic)
# ================================================================

class Utils:
    """
    NT-Tech helper utilities.
    ASCII-only, deterministic, safe conversions.
    """

    # ------------------------------------------------------------
    # Safe float conversion
    # ------------------------------------------------------------
    @staticmethod
    def safe_float(v):
        try:
            return float(v)
        except Exception:
            return 0.0

    # ------------------------------------------------------------
    # Safe int conversion
    # ------------------------------------------------------------
    @staticmethod
    def safe_int(v):
        try:
            return int(v)
        except Exception:
            return 0

    # ------------------------------------------------------------
    # ASCII-only string sanitizer
    # ------------------------------------------------------------
    @staticmethod
    def to_ascii(s):
        try:
            return str(s).encode("ascii", errors="ignore").decode("ascii")
        except Exception:
            return ""

    # ------------------------------------------------------------
    # Smart rounding
    # ------------------------------------------------------------
    @staticmethod
    def round_smart(v, digits=6):
        try:
            return round(float(v), digits)
        except Exception:
            return 0.0

    # ------------------------------------------------------------
    # Clamp value between min and max
    # ------------------------------------------------------------
    @staticmethod
    def clamp(v, vmin, vmax):
        try:
            x = float(v)
        except Exception:
            return vmin
        if x < vmin:
            return vmin
        if x > vmax:
            return vmax
        return x

    # ------------------------------------------------------------
    # Format number safely
    # ------------------------------------------------------------
    @staticmethod
    def fmt(v, digits=6):
        try:
            return round(float(v), digits)
        except Exception:
            return 0.0
