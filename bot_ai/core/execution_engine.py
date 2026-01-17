# bot_ai/core/execution_engine.py
# ⚙️ ExecutionEngine без автозакрытия в режиме live

import pandas as pd

class ExecutionEngine:
    def __init__(self, sl_pct=0.01, tp_pct=0.02, mode="backtest"):
        """
        sl_pct — стоп-лосс в процентах от entry (если не задан явно)
        tp_pct — тейк-профит в процентах от entry (если не задан явно)
        mode — режим исполнения: backtest / paper / live
        """
        self.sl_pct = sl_pct
        self.tp_pct = tp_pct
        self.mode = mode

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Исполняет сигналы по рынку. В режиме live — только лог входа.
        В режиме backtest/paper — закрывает сделку при достижении SL или TP.
        """
        trades = []

        for i, row in df.iterrows():
            if row.get("signal", 0) != 1:
                continue

            entry_time = i
            entry_price = row["entry"]
            stop_price = row.get("stop", entry_price * (1 - self.sl_pct))
            target_price = row.get("target", entry_price * (1 + self.tp_pct))
            size = row.get("size", 1)

            if self.mode == "live":
                # В live-режиме — только лог входа, без фиктивного выхода
                trades.append({
                    "entry_time": entry_time,
                    "exit_time": None,
                    "entry_price": entry_price,
                    "exit_price": None,
                    "pnl": None,
                    "size": round(size, 4),
                    "rrr": None,
                    "sl": stop_price,
                    "tp": target_price,
                    "status": "LIVE_SIGNAL"
                })
                continue

            # Поиск свечи, где сработал SL или TP
            exit_time = None
            exit_price = None

            for j in df.index[df.index.get_loc(i)+1:]:
                low = df.loc[j, "low"]
                high = df.loc[j, "high"]

                if low <= stop_price:
                    exit_time = j
                    exit_price = stop_price
                    break
                elif high >= target_price:
                    exit_time = j
                    exit_price = target_price
                    break

            if exit_time is None:
                continue  # сделка не закрылась — пропускаем

            pnl = (exit_price - entry_price) * size

            trades.append({
                "entry_time": entry_time,
                "exit_time": exit_time,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "pnl": round(pnl, 2),
                "size": round(size, 4),
                "rrr": round(abs(target_price - entry_price) / abs(entry_price - stop_price), 2),
                "sl": stop_price,
                "tp": target_price,
                "status": "EXECUTED"
            })

        return pd.DataFrame(trades)
