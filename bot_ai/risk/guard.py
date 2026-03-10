# ============================================
# File: bot_ai/risk/guard.py
# Purpose: RiskGuard with daily loss, volume, and cooldown checks
# Format: UTF-8 without BOM
# ASCII only (no Cyrillic)
# ============================================

import csv
from pathlib import Path
from .cooldown import Cooldown


class RiskGuard:
    def __init__(self, cfg):
        risk_cfg = getattr(cfg, "risk", {})

        # Daily loss
        self.max_daily_loss_enabled = getattr(risk_cfg, "max_daily_loss_enabled", False)
        self.max_daily_loss = getattr(risk_cfg, "max_daily_loss", None)

        # Volume
        self.min_24h_volume_usdt = getattr(risk_cfg, "min_24h_volume_usdt", None)

        # Cooldown stored inside logs/ to isolate tests
        cooldown_minutes = getattr(risk_cfg, "cooldown_minutes", 5)
        cooldown_path = Path("logs") / "cooldown.json"
        cooldown_path.parent.mkdir(parents=True, exist_ok=True)

        self.cooldown = Cooldown(
            path=str(cooldown_path),
            cooldown_hours=cooldown_minutes / 60
        )

        # Block log
        self.log_path = Path("logs") / "risk_blocks.csv"
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def _log_block(self, ctx, reason, details):
        file_exists = self.log_path.exists()
        with self.log_path.open("a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["symbol", "reason", "details", "mode"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "symbol": getattr(ctx, "symbol", "UNKNOWN"),
                "reason": reason,
                "details": details,
                "mode": getattr(ctx, "mode", "unknown"),
            })

    def check(self, ctx):
        # 1) Daily loss
        if self.max_daily_loss_enabled and self.max_daily_loss is not None:
            if getattr(ctx, "daily_loss", 0) >= self.max_daily_loss:
                self._log_block(ctx, "daily_loss", "daily loss limit exceeded")
                return False

        # 2) Volume
        if self.min_24h_volume_usdt is not None:
            if getattr(ctx, "vol24h_usdt", 0) < self.min_24h_volume_usdt:
                self._log_block(ctx, "low_volume", "volume below threshold")
                return False

        # 3) Cooldown
        if self.cooldown.is_blocked(ctx.symbol):
            self._log_block(ctx, "cooldown", "cooldown active")
            return False

        # 4) Update cooldown
        self.cooldown.update(ctx.symbol)
        return True
