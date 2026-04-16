# ================================================================
# File: bot_ai/execution/risk_state.py
# NT-Tech RiskState 1.0
# - Tracks equity, pnl, exposure, streak, kill-switch
# ASCII-only, deterministic
# ================================================================

class RiskState:
    """
    Pure state container for RiskEngine.
    Handles:
      - equity
      - daily/weekly pnl
      - exposure
      - losing streak
      - kill-switch
    """

    def __init__(
        self,
        initial_equity,
        max_daily_loss_pct,
        max_weekly_loss_pct,
        max_losing_streak,
        streak_loss_pct,
    ):
        self.equity = float(initial_equity)
        self.daily_pnl = 0.0
        self.weekly_pnl = 0.0

        self.open_exposure = 0.0

        self.max_daily_loss_pct = float(max_daily_loss_pct)
        self.max_weekly_loss_pct = float(max_weekly_loss_pct)

        self.max_losing_streak = int(max_losing_streak)
        self.streak_loss_pct = float(streak_loss_pct)

        self.current_losing_streak = 0
        self.current_streak_loss = 0.0

        self.kill_switch_active = False

    # ------------------------------------------------------------
    # Equity and PnL
    # ------------------------------------------------------------

    def update_equity(self, new_equity):
        self.equity = float(new_equity)

    def register_realized_pnl(self, pnl):
        self.equity += pnl
        self.daily_pnl += pnl
        self.weekly_pnl += pnl

        if pnl < 0:
            self.current_losing_streak += 1
            self.current_streak_loss += pnl
        else:
            self.current_losing_streak = 0
            self.current_streak_loss = 0.0

        self._check_loss_limits()
        self._check_streak_kill_switch()

    def reset_daily_pnl(self):
        self.daily_pnl = 0.0

    def reset_weekly_pnl(self):
        self.weekly_pnl = 0.0

    # ------------------------------------------------------------
    # Exposure
    # ------------------------------------------------------------

    def register_open_exposure(self, notional):
        self.open_exposure += abs(notional)

    def register_close_exposure(self, notional):
        self.open_exposure -= abs(notional)
        if self.open_exposure < 0:
            self.open_exposure = 0.0

    # ------------------------------------------------------------
    # Kill-switch logic
    # ------------------------------------------------------------

    def _check_loss_limits(self):
        if self.equity <= 0:
            self.kill_switch_active = True
            return

        daily_dd = -self.daily_pnl / self.equity if self.daily_pnl < 0 else 0.0
        weekly_dd = -self.weekly_pnl / self.equity if self.weekly_pnl < 0 else 0.0

        if daily_dd >= self.max_daily_loss_pct:
            self.kill_switch_active = True

        if weekly_dd >= self.max_weekly_loss_pct:
            self.kill_switch_active = True

    def _check_streak_kill_switch(self):
        if self.equity <= 0:
            self.kill_switch_active = True
            return

        if self.current_losing_streak <= 0:
            return

        streak_dd = -self.current_streak_loss / self.equity if self.current_streak_loss < 0 else 0.0

        if (
            self.current_losing_streak >= self.max_losing_streak
            and streak_dd >= self.streak_loss_pct
        ):
            self.kill_switch_active = True

    def is_kill_switch_active(self):
        return self.kill_switch_active

    def reset_kill_switch(self):
        self.kill_switch_active = False
        self.current_losing_streak = 0
        self.current_streak_loss = 0.0
