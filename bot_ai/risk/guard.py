import logging
import time
import csv
from datetime import datetime
from pathlib import Path
from tzlocal import get_localzone

local_tz = get_localzone()

class RiskGuard:
    def __init__(self, cfg, logger=None, notifier=None,
                 risk_log_file: str = "risk_log.csv",
                 risk_pass_log_file: str = "risk_pass_log.csv"):
        self.cfg = cfg
        self.logger = logger or logging.getLogger(__name__)
        self.notifier = notifier
        self.risk_cfg = cfg.get("risk", default={})
        self.last_trade_time = 0
        self.open_positions = 0
        self.total_loss_pct = 0
        self.daily_loss = 0.0
        self.kill_switch_triggered = False
        self.cooldowns = {}  # {symbol: datetime}
        self.risk_log_file = Path(risk_log_file)
        self.risk_pass_log_file = Path(risk_pass_log_file)

    def check(self, ctx):
        """Check trade against risk management rules."""

        # 1. Kill-switch
        if self.kill_switch_triggered:
            return self._deny("Kill-switch is active - trades are blocked")

        # 2. Minimum 24h volume
        min_vol = self.risk_cfg.get("min_24h_volume_usdt", 0)
        if ctx.vol24h_usdt < min_vol:
            return self._deny(f"Volume {ctx.vol24h_usdt} < {min_vol}")

        # 3. Maximum spread
        max_spread = self.risk_cfg.get("max_spread_pct", 100)
        if ctx.spread_pct > max_spread:
            return self._deny(f"Spread {ctx.spread_pct}% > {max_spread}%")

        # 4. Maximum daily loss
        max_daily_loss_pct = self.risk_cfg.get("max_daily_loss_pct", 100)
        if ctx.daily_pnl_usdt < 0:
            loss_pct = abs(ctx.daily_pnl_usdt) / ctx.equity_usdt * 100
            if loss_pct > max_daily_loss_pct:
                return self._deny(f"Daily loss {loss_pct:.2f}% > {max_daily_loss_pct}%")

        # 5. Kill-switch by total loss
        kill_switch_loss_pct = self.risk_cfg.get("kill_switch_loss_pct", 100)
        if self.total_loss_pct > kill_switch_loss_pct:
            self.kill_switch_triggered = True
            return self._deny(f"Total loss {self.total_loss_pct:.2f}% > {kill_switch_loss_pct}%")

        # 6. Max open positions
        max_positions = self.risk_cfg.get("max_positions", 999)
        if self.open_positions >= max_positions:
            return self._deny(f"Open positions {self.open_positions} >= {max_positions}")

        # 7. Risk per trade (log only)
        risk_per_trade_pct = self.risk_cfg.get("risk_per_trade_pct", 100)
        self._log(f"Risk per trade {risk_per_trade_pct}%")

        # 8. Max position size
        max_position_size_pct = self.risk_cfg.get("max_position_size_pct", 100)
        if (ctx.price / ctx.equity_usdt * 100) > max_position_size_pct:
            return self._deny(f"Position size > {max_position_size_pct}% of equity")

        # 9. Cooldown between trades
        cooldown_minutes = self.risk_cfg.get("cooldown_minutes", 0)
        if cooldown_minutes > 0:
            elapsed = (time.time() - self.last_trade_time) / 60
            if elapsed < cooldown_minutes:
                return self._deny(f"Cooldown {cooldown_minutes} min, only {elapsed:.1f} min passed")

        # If all checks passed
        self._log("Trade allowed")
        self.last_trade_time = time.time()
        self._log_pass("Trade allowed")
        return True

    def _deny(self, reason):
        if self.logger:
            self.logger.warning(f"[RiskGuard] DENY: {reason}")
        if self.notifier:
            self.notifier.alert(f"X {reason}")

        # Log deny to CSV
        self._log_to_csv(self.risk_log_file, reason)
        return False

    def _log(self, msg):
        if self.logger:
            self.logger.info(f"[RiskGuard] {msg}")
        if self.notifier:
            self.notifier.alert(f"INFO {msg}")

    def _log_pass(self, msg):
        self._log_to_csv(self.risk_pass_log_file, msg)

    def _log_to_csv(self, file_path: Path, message: str):
        file_exists = file_path.exists()
        with file_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp", "message"])
            writer.writerow([datetime.now(local_tz).isoformat(), message])