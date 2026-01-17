# ============================================
# File: bot_ai/risk/risk_guard.py
# Назначение: контроль рисков и блокировка сделок
# ============================================

import csv
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TradeContext:
    def __init__(self, symbol, side, price, equity_usdt,
                 daily_pnl_usdt=0, spread_pct=0, vol24h_usdt=0):
        self.symbol = symbol
        self.side = side.lower() if isinstance(side, str) else "flat"
        self.price = price
        self.equity_usdt = equity_usdt
        self.daily_pnl_usdt = daily_pnl_usdt
        self.spread_pct = spread_pct
        self.vol24h_usdt = vol24h_usdt

class RiskGuard:
    def __init__(self, cfg):
        self.cfg = cfg

    def check(self, ctx: TradeContext) -> (bool, str):
        if ctx.side not in {"buy", "sell", "flat"}:
            reason = f"Неизвестное значение side: '{ctx.side}'"
            logger.warning(f"[RiskGuard] ОТКАЗ: {reason}")
            return False, reason

        if ctx.side == "flat":
            reason = "Сторона сделки — flat (вне позиции), вход не требуется"
            logger.info(f"[RiskGuard] ПРОПУСК: {reason}")
            return False, reason

        equity = ctx.equity_usdt
        risk_cfg = self.cfg.get("risk", {})

        risk_pct = risk_cfg.get("risk_per_trade_pct", 1.0)
        max_usdt = risk_cfg.get("max_per_trade_usdt", equity)
        max_pos_pct = risk_cfg.get("max_position_size_pct", 100)

        risk_usdt = min(equity * (risk_pct / 100.0), max_usdt)
        position_value_usdt = risk_usdt

        if position_value_usdt > equity * (max_pos_pct / 100.0):
            reason = f"Стоимость позиции {
                position_value_usdt:.2f} > {max_pos_pct}% от equity {equity}"
            logger.warning(f"[RiskGuard] ОТКАЗ: {reason}")
            return False, reason

        max_daily_loss = risk_cfg.get("daily_loss_limit_usdt", 0)
        if max_daily_loss and ctx.daily_pnl_usdt < -max_daily_loss:
            reason = f"Дневной убыток {
                ctx.daily_pnl_usdt} < лимит {max_daily_loss}"
            logger.warning(f"[RiskGuard] ОТКАЗ: {reason}")
            return False, reason

        max_spread = risk_cfg.get("max_spread_pct", 100)
        if ctx.spread_pct > max_spread:
            reason = f"Спред {ctx.spread_pct:.2f}% > {max_spread}%"
            logger.warning(f"[RiskGuard] ОТКАЗ: {reason}")
            return False, reason

        min_vol = risk_cfg.get("min_24h_volume_usdt", 0)
        if ctx.vol24h_usdt < min_vol:
            reason = f"Объём {ctx.vol24h_usdt} < {min_vol}"
            logger.warning(f"[RiskGuard] ОТКАЗ: {reason}")
            return False, reason

        return True, "OK"

class RiskGuardWithLogging(RiskGuard):
    """
    Расширение RiskGuard: пишет все отказы в risk_blocks.csv с конкретной причиной
    """

    def __init__(self, cfg, log_file="risk_blocks.csv"):
        super().__init__(cfg)
        self.log_file = log_file
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["symbol", "side", "price", "equity_usdt", "reason"])

    def check(self, ctx: TradeContext) -> bool:
        result, reason = super().check(ctx)
        if not result:
            with open(self.log_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [ctx.symbol, ctx.side, ctx.price, ctx.equity_usdt, reason])
        return result

