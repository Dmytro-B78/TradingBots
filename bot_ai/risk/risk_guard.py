# ============================================
# File: bot_ai/risk/risk_guard.py
# Purpose: Unified RiskGuard implementation matching test suite
# Format: UTF-8 without BOM
# ASCII only
# ============================================

import json
from pathlib import Path
from datetime import datetime, timedelta


class TradeContext:
    """
    TradeContext used by tests.
    """

    def __init__(
        self,
        symbol="BTCUSDT",
        daily_loss=0.0,
        vol24h_usdt=0.0,
        spread_pct=0.0,
        equity_usdt=0.0,
        price=0.0,
        mode="paper",
        kill_switch=False,
        max_positions=0,
        position_size=1.0,
        risk_per_trade=0.0,
        total_loss=0.0
    ):
        self.symbol = symbol
        self.daily_loss = daily_loss
        self.vol24h_usdt = vol24h_usdt
        self.spread_pct = spread_pct
        self.equity_usdt = equity_usdt
        self.price = price
        self.mode = mode
        self.kill_switch = kill_switch
        self.max_positions = max_positions
        self.position_size = position_size
        self.risk_per_trade = risk_per_trade
        self.total_loss = total_loss


class RiskGuard:
    """
    RiskGuard implementation matching test suite.
    """

    def __init__(self, cfg):
        risk_cfg = getattr(cfg, "risk", {})

        self.max_daily_loss_enabled = getattr(risk_cfg, "max_daily_loss_enabled", False)
        self.max_daily_loss = getattr(risk_cfg, "max_daily_loss", None)

        self.min_24h_volume_usdt = getattr(risk_cfg, "min_24h_volume_usdt", None)

        self.max_positions_limit = getattr(risk_cfg, "max_positions", None)
        self.max_risk_per_trade = getattr(risk_cfg, "max_risk_per_trade", None)
        self.max_spread_pct = getattr(risk_cfg, "max_spread", None)

        self.max_total_loss_enabled = getattr(risk_cfg, "max_total_loss_enabled", False)
        self.max_total_loss = getattr(risk_cfg, "max_total_loss", None)

        cooldown_minutes = getattr(risk_cfg, "cooldown_minutes", 5)
        self.cooldown_seconds = cooldown_minutes * 60
        self.cooldown_path = Path("cooldown.json")

        self.blocked_reasons = []

    def get_blocked_reasons(self):
        return self.blocked_reasons

    # ----------------------------------------
    # Cooldown helpers
    # ----------------------------------------

    def _load_cooldown(self):
        if not self.cooldown_path.exists():
            return {}
        try:
            with self.cooldown_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def _save_cooldown(self, data):
        with self.cooldown_path.open("w", encoding="utf-8") as f:
            json.dump(data, f)

    def _is_cooldown_blocked(self, symbol):
        data = self._load_cooldown()
        ts = data.get(symbol)
        if not ts:
            return False
        last = datetime.fromisoformat(ts)
        if datetime.utcnow() - last < timedelta(seconds=self.cooldown_seconds):
            return True
        return False

    def _update_cooldown(self, symbol):
        data = self._load_cooldown()
        data[symbol] = datetime.utcnow().isoformat()
        self._save_cooldown(data)

    # ----------------------------------------
    # Main check
    # ----------------------------------------

    def check(self, ctx):
        self.blocked_reasons = []

        # Kill switch
        if getattr(ctx, "kill_switch", False):
            self.blocked_reasons.append("Kill switch activated")
            return False

        # Daily loss
        if self.max_daily_loss_enabled and self.max_daily_loss is not None:
            if getattr(ctx, "daily_loss", 0) >= self.max_daily_loss:
                self.blocked_reasons.append("Max daily loss exceeded")
                return False

        # Total loss
        if self.max_total_loss_enabled and self.max_total_loss is not None:
            if getattr(ctx, "total_loss", 0) >= self.max_total_loss:
                self.blocked_reasons.append("Max total loss exceeded")
                return False

        # Volume
        if self.min_24h_volume_usdt is not None:
            if getattr(ctx, "vol24h_usdt", 0) < self.min_24h_volume_usdt:
                self.blocked_reasons.append("Low 24h volume")
                return False

        # Max positions
        if self.max_positions_limit is not None:
            if getattr(ctx, "max_positions", 0) >= self.max_positions_limit:
                self.blocked_reasons.append("Max positions reached")
                return False

        # Position size
        if getattr(ctx, "position_size", 0) <= 0:
            self.blocked_reasons.append("Invalid position size")
            return False

        # Risk per trade
        if self.max_risk_per_trade is not None:
            if getattr(ctx, "risk_per_trade", 0) > self.max_risk_per_trade:
                self.blocked_reasons.append("Risk per trade too high")
                return False

        # Spread
        if self.max_spread_pct is not None:
            if getattr(ctx, "spread_pct", 0) > self.max_spread_pct:
                self.blocked_reasons.append("Spread too wide")
                return False

        # Cooldown
        if self._is_cooldown_blocked(ctx.symbol):
            self.blocked_reasons.append("Cooldown active")
            return False

        # Update cooldown
        self._update_cooldown(ctx.symbol)
        return True
