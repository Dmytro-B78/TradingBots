# ================================================================
# File: bot_ai/engine/offline_log_analyzer_full.py
# NT-Tech Full Analyzer 2.1 (ASCII-only)
# - Reads extended offline_log.txt
# - Uses ONLY the last OfflineRunner session
# - Extracts trades, meta_signals, risk_actions
# - Computes:
#     * equity curve
#     * PnL distribution
#     * trade duration
#     * ATR regime stats
#     * local/global regime stats
#     * confidence distribution
# - Deterministic ASCII output
# ================================================================

import json
import os
from collections import Counter


class FullAnalyzer:
    def __init__(self, log_path="logs/offline_log.txt"):
        self.log_path = log_path

        self.trades = []
        self.meta_signals = []
        self.risk_actions = []

        self.equity = []
        self.initial_equity = 10000.0

    # ============================================================
    # Load log (only last session)
    # ============================================================

    def load(self):
        if not os.path.exists(self.log_path):
            raise FileNotFoundError(f"log not found: {self.log_path}")

        # We keep ONLY the last session between "OfflineRunner start" and "OfflineRunner end"
        current_trades = []
        current_meta = []
        current_risk = []
        in_session = False

        with open(self.log_path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line:
                    continue

                if line.startswith("OfflineRunner start"):
                    # start of a new session: reset buffers
                    in_session = True
                    current_trades = []
                    current_meta = []
                    current_risk = []
                    continue

                if line.startswith("OfflineRunner end"):
                    # end of session: keep last one
                    in_session = False
                    self.trades = current_trades
                    self.meta_signals = current_meta
                    self.risk_actions = current_risk
                    continue

                if not in_session:
                    # ignore lines outside sessions
                    continue

                if not line.startswith("{"):
                    continue

                try:
                    obj = json.loads(line)
                except Exception:
                    continue

                kind = obj.get("kind")

                if kind == "trade":
                    current_trades.append(obj)
                elif kind == "meta_signal":
                    current_meta.append(obj)
                elif kind == "risk_action":
                    current_risk.append(obj)

        # Fallback: if no explicit "OfflineRunner end" was found but we have data in buffers
        if current_trades or current_meta or current_risk:
            self.trades = current_trades
            self.meta_signals = current_meta
            self.risk_actions = current_risk

    # ============================================================
    # Equity curve
    # ============================================================

    def compute_equity(self):
        eq = self.initial_equity
        self.equity = [eq]

        for t in self.trades:
            pnl = t.get("pnl_abs")
            if pnl is None:
                continue
            eq += pnl
            self.equity.append(eq)

    def print_equity_curve(self):
        print("=" * 60)
        print("Equity Curve (ASCII)")
        print("=" * 60)

        if not self.equity:
            print("(no equity data)")
            return

        eq_min = min(self.equity)
        eq_max = max(self.equity)
        span = eq_max - eq_min if eq_max != eq_min else 1.0

        width = 60
        for v in self.equity:
            pos = int((v - eq_min) / span * (width - 1))
            line = [" "] * width
            line[pos] = "*"
            print("".join(line))

    # ============================================================
    # Stats
    # ============================================================

    def print_trade_stats(self):
        print("=" * 60)
        print("Trade Stats")
        print("=" * 60)

        if not self.trades:
            print("(no trades)")
            return

        pnl_list = []
        durations = []

        atr_1h = []
        atr_4h = []
        local_regime = Counter()
        global_regime = Counter()
        confidence = []

        for t in self.trades:
            pnl = t.get("pnl_pct")
            if pnl is not None:
                pnl_list.append(pnl)

            entry_ms = t.get("entry_time_ms")
            exit_ms = t.get("exit_time_ms")
            if entry_ms is not None and exit_ms is not None:
                durations.append(exit_ms - entry_ms)

            atr1 = t.get("atr_1h_entry")
            atr4 = t.get("atr_4h_entry")
            if atr1 is not None:
                atr_1h.append(atr1)
            if atr4 is not None:
                atr_4h.append(atr4)

            lr = t.get("local_regime_entry")
            gr = t.get("global_regime_entry")
            if lr:
                local_regime[lr] += 1
            if gr:
                global_regime[gr] += 1

            conf = t.get("confidence_entry")
            if conf is not None:
                confidence.append(conf)

        if pnl_list:
            print(f"Trades: {len(pnl_list)}")
            print(f"Avg PnL %: {sum(pnl_list)/len(pnl_list):.4f}")
            print(f"Win rate: {sum(1 for x in pnl_list if x>0)/len(pnl_list)*100:.2f}%")
            print(f"Best trade %: {max(pnl_list):.4f}")
            print(f"Worst trade %: {min(pnl_list):.4f}")

        if durations:
            print(f"Avg duration (ms): {sum(durations)/len(durations):.2f}")

        if atr_1h:
            print(f"Avg ATR 1h: {sum(atr_1h)/len(atr_1h):.6f}")
        if atr_4h:
            print(f"Avg ATR 4h: {sum(atr_4h)/len(atr_4h):.6f}")

        print("Local regime distribution:")
        for k, v in local_regime.items():
            print(f"  {k}: {v}")

        print("Global regime distribution:")
        for k, v in global_regime.items():
            print(f"  {k}: {v}")

        if confidence:
            print(f"Avg confidence: {sum(confidence)/len(confidence):.4f}")

    # ============================================================
    # Histogram helper
    # ============================================================

    def print_histogram(self, title, values, bins=20):
        print("=" * 60)
        print(title)
        print("=" * 60)

        if not values:
            print("(none)")
            return

        vmin = min(values)
        vmax = max(values)
        span = vmax - vmin if vmax != vmin else 1.0

        counts = [0] * bins
        for v in values:
            idx = int((v - vmin) / span * (bins - 1))
            counts[idx] += 1

        max_count = max(counts)
        if max_count == 0:
            for i in range(bins):
                print(f"{i:02d} ")
            return

        for i, c in enumerate(counts):
            bar = "*" * int(c / max_count * 50)
            print(f"{i:02d} {bar}")

    # ============================================================
    # Main
    # ============================================================

    def run(self):
        self.load()
        self.compute_equity()

        print("=" * 60)
        print("Full Analyzer 2.1 Summary")
        print("=" * 60)
        print(f"Trades: {len(self.trades)}")
        print(f"Meta signals: {len(self.meta_signals)}")
        print(f"Risk actions: {len(self.risk_actions)}")

        self.print_equity_curve()
        self.print_trade_stats()

        pnl_values = [t.get("pnl_pct") for t in self.trades if t.get("pnl_pct") is not None]
        self.print_histogram("PnL % Histogram", pnl_values)

        durations = [
            t.get("exit_time_ms") - t.get("entry_time_ms")
            for t in self.trades
            if t.get("entry_time_ms") is not None and t.get("exit_time_ms") is not None
        ]
        self.print_histogram("Trade Duration Histogram (ms)", durations)


if __name__ == "__main__":
    analyzer = FullAnalyzer("logs/offline_log.txt")
    analyzer.run()
