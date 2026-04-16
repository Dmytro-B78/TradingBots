# ================================================================
# File: bot_ai/engine/offline_runner.py
# NT-Tech Offline Runner 7.6-F — intrabar-aware exits
# ================================================================

import csv
import json
import os
from bot_ai.strategy.meta_strategy import MetaStrategy
from bot_ai.risk.risk_guard import RiskGuard


def load_csv(path):
    rows = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        for r in reader:
            if len(r) < 5:
                continue
            try:
                rows.append({
                    "timestamp": int(float(r[0])),
                    "open": float(r[1]),
                    "high": float(r[2]),
                    "low": float(r[3]),
                    "close": float(r[4]),
                })
            except:
                continue
    return rows


def run():
    csv_path = "C:\\TradingBots\\candles\\compiled\\SOLUSDT-1h.csv"
    candles = load_csv(csv_path)

    strategy = MetaStrategy()
    risk = RiskGuard()

    log_path = "logs/offline_log.txt"
    if os.path.exists(log_path):
        os.remove(log_path)

    meta_signal_count = 0
    risk_action_count = 0
    trade_count = 0

    current_position = None
    current_trade = None

    with open(log_path, "w", encoding="utf-8") as log:
        log.write("OfflineRunner start\n")

        for i, c in enumerate(candles):
            ts = c["timestamp"]
            close_price = c["close"]

            meta_state = strategy.compute_meta_state(c)
            meta_signal = strategy.compute_meta_signal(meta_state)

            if meta_signal:
                meta_signal_count += 1

                log.write(json.dumps({
                    "kind": "meta_signal",
                    "signal": meta_signal.get("signal"),
                    "regime": meta_signal.get("regime"),
                    "global_regime": meta_signal.get("global_regime"),
                    "atr_1h": meta_signal.get("atr_1h"),
                    "atr_4h": meta_signal.get("atr_4h"),
                    "confidence": meta_signal.get("confidence")
                }) + "\n")

                risk_action = risk.process_meta_signal(meta_signal)
                if risk_action:
                    risk_action_count += 1

                    log.write(json.dumps({
                        "kind": "risk_action",
                        "action": risk_action.get("action")
                    }) + "\n")

                    action = risk_action.get("action")

                    if action == "OPEN_LONG":
                        if current_position is None:
                            current_position = "LONG"
                            current_trade = {
                                "entry_price": close_price,
                                "entry_index": i,
                                "entry_time_ms": ts,
                                "atr_1h": meta_signal.get("atr_1h"),
                                "atr_4h": meta_signal.get("atr_4h"),
                                "regime": meta_signal.get("regime"),
                                "global_regime": meta_signal.get("global_regime"),
                                "confidence": meta_signal.get("confidence"),
                            }

                    elif action == "CLOSE_LONG":
                        if current_position == "LONG" and current_trade is not None:
                            current_position = None

                            entry = current_trade["entry_price"]
                            exitp = meta_signal.get("exit_price", close_price)
                            pnl_pct = (exitp - entry) / entry * 100.0 if entry else None
                            bars = i - current_trade["entry_index"]

                            log.write(json.dumps({
                                "kind": "trade",
                                "entry": round(entry, 6),
                                "exit": round(exitp, 6),
                                "pnl_pct": round(pnl_pct, 6),
                                "duration_bars": bars,
                                "entry_time_ms": current_trade["entry_time_ms"],
                                "exit_time_ms": ts,
                                "atr_1h_entry": round(current_trade["atr_1h"], 6) if current_trade["atr_1h"] else None,
                                "atr_4h_entry": round(current_trade["atr_4h"], 6) if current_trade["atr_4h"] else None,
                                "local_regime_entry": current_trade["regime"],
                                "global_regime_entry": current_trade["global_regime"],
                                "confidence_entry": round(current_trade["confidence"], 6) if current_trade["confidence"] else None
                            }) + "\n")

                            trade_count += 1
                            current_trade = None

        log.write("OfflineRunner end\n")

    summary = {
        "kind": "summary",
        "csv": csv_path,
        "candles": len(candles),
        "meta_signal_count": meta_signal_count,
        "risk_action_count": risk_action_count,
        "trade_count": trade_count,
    }

    print(json.dumps(summary))


if __name__ == "__main__":
    run()
