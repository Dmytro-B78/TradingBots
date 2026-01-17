# -*- coding: utf-8 -*-
# === bot_ai/risk/position_manager.py ===
# Управление открытой позицией: открытие, трейлинг-стоп, SL/TP, частичная фиксация

from datetime import datetime

class PositionManager:
    def __init__(self):
        self.active_position = None
        self.trailing_sl_distance = None
        self.partial_taken = False
        self.partial_pct = 0.5
        self.move_sl_to_be = True

    def open(
            self,
            symbol,
            side,
            entry,
            sl,
            tp1,
            tp2,
            qty,
            strategy,
            trailing_sl=None,
            partial_pct=0.5,
            move_sl_to_be=True):
        self.active_position = {
            "symbol": symbol,
            "side": side,
            "entry": entry,
            "sl": sl,
            "tp1": tp1,
            "tp2": tp2,
            "qty": qty,
            "strategy": strategy,
            "opened_at": datetime.utcnow().isoformat()
        }
        self.trailing_sl_distance = trailing_sl
        self.partial_taken = False
        self.partial_pct = partial_pct
        self.move_sl_to_be = move_sl_to_be

    def is_open(self):
        return self.active_position is not None

    def update_trailing_sl(self, current_price):
        if not self.active_position or not self.trailing_sl_distance:
            return

        side = self.active_position["side"]
        sl = self.active_position["sl"]

        if side == "long":
            new_sl = current_price - self.trailing_sl_distance
            if new_sl > sl:
                self.active_position["sl"] = round(new_sl, 2)
        elif side == "short":
            new_sl = current_price + self.trailing_sl_distance
            if new_sl < sl:
                self.active_position["sl"] = round(new_sl, 2)

    def check_exit(self, current_price):
        if not self.active_position:
            return None

        side = self.active_position["side"]
        sl = self.active_position["sl"]
        tp1 = self.active_position["tp1"]
        tp2 = self.active_position["tp2"]
        entry = self.active_position["entry"]
        qty = self.active_position["qty"]

        # === Частичная фиксация на TP1 ===
        if not self.partial_taken:
            if (side == "long" and current_price >= tp1) or (
                    side == "short" and current_price <= tp1):
                partial_qty = round(qty * self.partial_pct, 6)
                pnl_pct = ((current_price - entry) / entry) * 100
                if side == "short":
                    pnl_pct *= -1
                pnl_usdt = round((pnl_pct / 100) * partial_qty * entry, 2)

                if self.move_sl_to_be:
                    self.active_position["sl"] = entry

                self.active_position["qty"] = round(qty - partial_qty, 6)
                self.partial_taken = True

                return {
                    "symbol": self.active_position["symbol"],
                    "side": side,
                    "entry": entry,
                    "exit": current_price,
                    "reason": "TP1 (partial)",
                    "pnl_pct": round(pnl_pct, 2),
                    "pnl_usdt": pnl_usdt,
                    "qty": partial_qty,
                    "strategy": self.active_position["strategy"],
                    "opened_at": self.active_position["opened_at"],
                    "closed_at": datetime.utcnow().isoformat()
                }

        # === Полный выход по SL или TP2 ===
        exit_reason = None
        if side == "long":
            if current_price <= sl:
                exit_reason = "SL"
            elif current_price >= tp2:
                exit_reason = "TP2"
        elif side == "short":
            if current_price >= sl:
                exit_reason = "SL"
            elif current_price <= tp2:
                exit_reason = "TP2"

        if exit_reason:
            pnl_pct = ((current_price - entry) / entry) * 100
            if side == "short":
                pnl_pct *= -1
            pnl_usdt = round(
                (pnl_pct / 100) * self.active_position["qty"] * entry, 2)

            result = {
                "symbol": self.active_position["symbol"],
                "side": side,
                "entry": entry,
                "exit": current_price,
                "reason": exit_reason,
                "pnl_pct": round(pnl_pct, 2),
                "pnl_usdt": pnl_usdt,
                "qty": self.active_position["qty"],
                "strategy": self.active_position["strategy"],
                "opened_at": self.active_position["opened_at"],
                "closed_at": datetime.utcnow().isoformat()
            }

            self.active_position = None
            self.trailing_sl_distance = None
            self.partial_taken = False
            return result

        return None
