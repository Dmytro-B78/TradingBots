# ============================================
# File: risk_guard.py
# Purpose: Centralized risk management system
# Format: UTF-8 without BOM, ASCII-only, ready for integration
# ============================================

class TradeContext:
    """
    Holds contextual trade data for risk evaluation.
    """
    def __init__(self):
        self.daily_loss = 0
        self.kill_switch = False
        self.volume = 0
        self.max_positions = 0
        self.position_size = 0
        self.risk_per_trade = 0
        self.spread = 0
        self.total_loss = 0


class RiskGuard:
    """
    Centralized risk control system with multiple blocking rules.
    """

    def __init__(self, config):
        self.config = config
        self.blocked_reasons = []

    def get_blocked_reasons(self):
        return self.blocked_reasons

    def check(self, ctx):
        """
        Evaluate all risk rules against the current trade context.

        Parameters:
            ctx (TradeContext): Current trade context

        Returns:
            bool: True if trade is allowed, False if blocked
        """
        self.blocked_reasons.clear()

        if self.block_daily_loss(ctx): return False
        if self.block_kill_switch(ctx): return False
        if self.block_low_volume(ctx): return False
        if self.block_max_positions(ctx): return False
        if self.block_position_size(ctx): return False
        if self.block_risk_per_trade(ctx): return False
        if self.block_spread(ctx): return False
        if self.block_total_loss(ctx): return False

        return True

    def block_daily_loss(self, ctx):
        if getattr(self.config.risk, "max_daily_loss_enabled", False):
            if ctx.daily_loss >= self.config.risk.max_daily_loss:
                self.blocked_reasons.append("Max daily loss exceeded")
                return True
        return False

    def block_kill_switch(self, ctx):
        if ctx.kill_switch:
            self.blocked_reasons.append("Kill switch activated")
            return True
        return False

    def block_low_volume(self, ctx):
        if ctx.volume < getattr(self.config.risk, "min_24h_volume_usdt", 0):
            self.blocked_reasons.append("Low 24h volume")
            return True
        return False

    def block_max_positions(self, ctx):
        if ctx.max_positions >= getattr(self.config.risk, "max_positions", 999):
            self.blocked_reasons.append("Max positions reached")
            return True
        return False

    def block_position_size(self, ctx):
        if ctx.position_size <= 0:
            self.blocked_reasons.append("Invalid position size")
            return True
        return False

    def block_risk_per_trade(self, ctx):
        if ctx.risk_per_trade > getattr(self.config.risk, "max_risk_per_trade", 1.0):
            self.blocked_reasons.append("Risk per trade too high")
            return True
        return False

    def block_spread(self, ctx):
        if ctx.spread > getattr(self.config.risk, "max_spread", 999):
            self.blocked_reasons.append("Spread too wide")
            return True
        return False

    def block_total_loss(self, ctx):
        if getattr(self.config.risk, "max_total_loss_enabled", False):
            if ctx.total_loss >= self.config.risk.max_total_loss:
                self.blocked_reasons.append("Max total loss exceeded")
                return True
        return False
