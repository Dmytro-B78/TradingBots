from dataclasses import dataclass
from datetime import datetime, timezone
import csv
import os
from .guard import RiskGuard

@dataclass
class TradeContext:
    """
    Контекст сделки, передаваемый в RiskGuard.
    """
    symbol: str
    side: str
    price: float
    equity_usdt: float
    daily_pnl_usdt: float
    spread_pct: float
    vol24h_usdt: float

class RiskGuardWithLogging(RiskGuard):
    """
    Расширенный RiskGuard с дополнительным CSV-логом причин блокировки сделки.
    """

    def __init__(self, config):
        # Передаём пути к логам в базовый RiskGuard, чтобы они создавались в рабочей директории
        super().__init__(
            cfg=config,
            risk_log_file="risk_log.csv",
            risk_pass_log_file="risk_pass_log.csv"
        )
        self.ext_block_log_path = os.path.join("logs", "risk_blocks_ext.csv")
        if not os.path.exists(self.ext_block_log_path):
            os.makedirs(os.path.dirname(self.ext_block_log_path), exist_ok=True)
            with open(self.ext_block_log_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "symbol", "side", "price",
                    "equity_usdt", "daily_pnl_usdt",
                    "spread_pct", "vol24h_usdt", "reason"
                ])

    def log_block_reason_ext(self, ctx: TradeContext, reason: str):
        """
        Записывает причину блокировки сделки в расширенный risk_blocks_ext.csv.
        """
        with open(self.ext_block_log_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now(timezone.utc).isoformat(),
                ctx.symbol,
                ctx.side,
                ctx.price,
                ctx.equity_usdt,
                ctx.daily_pnl_usdt,
                ctx.spread_pct,
                ctx.vol24h_usdt,
                reason
            ])

    def check(self, ctx: TradeContext) -> bool:
        """
        Переопределённая проверка возможности сделки.
        Если блокируем — пишем в расширенный CSV.
        Разрешённые сделки логируются базовым классом в risk_log.csv.
        """
        allowed = super().check(ctx)
        if allowed:
            # Гарантируем, что risk_log.csv существует
            if not self.risk_log_file.exists():
                self._log_to_csv(self.risk_log_file, "Сделка разрешена")
        else:
            self.log_block_reason_ext(ctx, getattr(ctx, "reason", "unknown"))
        return allowed
