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

        # Универсальная обработка: Config или dict
        if hasattr(cfg, "get"):
            try:
                self.risk_cfg = cfg.get("risk", default={})
            except TypeError:
                self.risk_cfg = cfg.get("risk", {})
        else:
            self.risk_cfg = {}

        self.last_trade_time = 0
        self.open_positions = 0
        self.total_loss_pct = 0
        self.daily_loss = 0.0
        self.kill_switch_triggered = False
        self.cooldowns = {}  # {symbol: timestamp}
        self.risk_log_file = Path(risk_log_file)
        self.risk_pass_log_file = Path(risk_pass_log_file)

    def check(self, ctx):
        """Проверка сделки на соответствие риск-менеджменту."""

        # 1. Kill-switch
        if self.kill_switch_triggered:
            return self._deny("Kill-switch активирован — сделки запрещены",
                              ctx=ctx, reason_code="kill_switch")

        # 2. Минимальный 24h объём
        min_vol = self.risk_cfg.get("min_24h_volume_usdt", 0)
        if ctx.vol24h_usdt < min_vol:
            return self._deny(f"Объём {ctx.vol24h_usdt} < {min_vol}",
                              ctx=ctx, reason_code="low_volume",
                              details=f"{ctx.vol24h_usdt} < {min_vol}")

        # 3. Максимальный спред
        max_spread = self.risk_cfg.get("max_spread_pct", 100)
        if ctx.spread_pct > max_spread:
            return self._deny(f"Спред {ctx.spread_pct}% > {max_spread}%",
                              ctx=ctx, reason_code="spread",
                              details=f"{ctx.spread_pct}% > {max_spread}%")

        # 4. Максимальный дневной убыток
        max_daily_loss_pct = self.risk_cfg.get("max_daily_loss_pct", 100)
        if ctx.daily_pnl_usdt < 0:
            loss_pct = abs(ctx.daily_pnl_usdt) / ctx.equity_usdt * 100
            if loss_pct > max_daily_loss_pct:
                return self._deny(
                    f"Дневной убыток {loss_pct:.2f}% > {max_daily_loss_pct}%",
                    ctx=ctx, reason_code="daily_loss",
                    details=f"{loss_pct:.2f}% > {max_daily_loss_pct}%",
                    current_loss=loss_pct, limit=max_daily_loss_pct
                )

        # 5. Kill-switch по общему убытку
        kill_switch_loss_pct = self.risk_cfg.get("kill_switch_loss_pct", 100)
        if self.total_loss_pct > kill_switch_loss_pct:
            self.kill_switch_triggered = True
            return self._deny(
                f"Общий убыток {self.total_loss_pct:.2f}% > {kill_switch_loss_pct}%",
                ctx=ctx, reason_code="total_loss",
                details=f"{self.total_loss_pct:.2f}% > {kill_switch_loss_pct}%",
                current_loss=self.total_loss_pct, limit=kill_switch_loss_pct
            )

        # 6. Лимит по количеству позиций
        max_positions = self.risk_cfg.get("max_positions", 999)
        if self.open_positions >= max_positions:
            return self._deny(f"Открытых позиций {self.open_positions} >= {max_positions}",
                              ctx=ctx, reason_code="max_positions",
                              details=f"{self.open_positions} >= {max_positions}")

        # 7. Риск на сделку (логируем)
        risk_per_trade_pct = self.risk_cfg.get("risk_per_trade_pct", 100)
        self._log(f"Риск на сделку {risk_per_trade_pct}%")

        # 8. Максимальный размер позиции
        max_position_size_pct = self.risk_cfg.get("max_position_size_pct", 100)
        if (ctx.price / ctx.equity_usdt * 100) > max_position_size_pct:
            return self._deny(f"Размер позиции > {max_position_size_pct}% от equity",
                              ctx=ctx, reason_code="position_size",
                              details=f"{ctx.price / ctx.equity_usdt * 100:.2f}% > {max_position_size_pct}%")

        # 9. Кулдаун между сделками (по символу)
        cooldown_minutes = self.risk_cfg.get("cooldown_minutes", 0)
        if cooldown_minutes > 0 and hasattr(ctx, "symbol"):
            last_trade_ts = self.cooldowns.get(ctx.symbol, 0)
            elapsed = (time.time() - last_trade_ts) / 60
            if elapsed < cooldown_minutes:
                return self._deny(f"Кулдаун {cooldown_minutes} мин, прошло {elapsed:.1f} мин",
                                  ctx=ctx, reason_code="cooldown",
                                  details=f"{elapsed:.1f} < {cooldown_minutes} мин")
            self.cooldowns[ctx.symbol] = time.time()

        # Если все проверки пройдены
        self._log("Сделка разрешена")
        self.last_trade_time = time.time()
        self._log_pass("Сделка разрешена")
        return True

    def _deny(self, reason, ctx=None, reason_code="generic", details="", current_loss=None, limit=None):
        if self.logger:
            self.logger.warning(f"[RiskGuard] ОТКАЗ: {reason}")
        if self.notifier:
            self.notifier.alert(f"❌ {reason}")
        self._log_to_csv(self.risk_log_file, reason)
        self._log_block_reason(ctx, reason_code, details, current_loss, limit)
        return False

    def _log(self, msg):
        if self.logger:
            self.logger.info(f"[RiskGuard] {msg}")
        if self.notifier:
            self.notifier.alert(f"ℹ️ {msg}")

    def _log_pass(self, msg):
        self._log_to_csv(self.risk_pass_log_file, msg)

    def _log_to_csv(self, file_path: Path, message: str):
        file_exists = file_path.exists()
        with file_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp", "message"])
            writer.writerow([datetime.now(local_tz).isoformat(), message])

    def _log_block_reason(self, ctx, reason_code, details="", current_loss=None, limit=None):
        """Логирование причин блокировки сделки в logs/risk_blocks.csv"""
        file_path = Path("logs") / "risk_blocks.csv"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_exists = file_path.exists()
        with file_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow([
                    "timestamp", "symbol", "reason", "details",
                    "mode", "current_loss", "limit"
                ])
            writer.writerow([
                datetime.now(local_tz).isoformat(),
                getattr(ctx, "symbol", "") if ctx else "",
                reason_code,
                details,
                getattr(ctx, "mode", getattr(self.cfg, "mode", "unknown")),
                current_loss if current_loss is not None else "",
                limit if limit is not None else ""
            ])
