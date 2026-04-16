# ================================================================
# File: bot_ai/engine/offline_log_analyzer.py
# NT-Tech Offline Log Analyzer 1.0 (ASCII-only)
# - Reads offline_log.txt
# - Parses JSON lines from OfflineRunner
# - Aggregates:
#     * meta_signal count
#     * risk_action count
#     * SKIP_OPEN reasons
#     * CLOSE_LONG reasons
#     * kill_switch occurrences
# - Deterministic ASCII output
# ================================================================

import json
import os
from collections import Counter, defaultdict


class OfflineLogAnalyzer:
    """
    Lite analyzer for OfflineRunner logs.

    Input:
      - offline_log.txt produced by OfflineRunner

    Output:
      - deterministic ASCII summary to stdout
    """

    def __init__(self, log_path="logs/offline_log.txt"):
        self.log_path = log_path

        self.meta_signal_count = 0
        self.risk_action_count = 0

        self.skip_open_reasons = Counter()
        self.close_reasons = Counter()
        self.kill_switch_events = 0

        self.raw_events = []

    # ============================================================
    # Load and parse
    # ============================================================

    def _load_lines(self):
        if not os.path.exists(self.log_path):
            raise FileNotFoundError(f"offline log not found: {self.log_path}")

        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                yield line

    def _parse_json(self, line):
        try:
            return json.loads(line)
        except Exception:
            return None

    # ============================================================
    # Analyze
    # ============================================================

    def analyze(self):
        for line in self._load_lines():
            obj = self._parse_json(line)
            if not isinstance(obj, dict):
                continue

            kind = obj.get("kind")

            if kind == "meta_signal":
                self.meta_signal_count += 1
                self.raw_events.append(obj)

            elif kind == "risk_action":
                self.risk_action_count += 1
                self._process_risk_action(obj)
                self.raw_events.append(obj)

            elif kind == "summary":
                # summary from OfflineRunner, can be used for cross-check
                self.raw_events.append(obj)

    def _process_risk_action(self, obj):
        ra = obj.get("risk_action") or {}
        action = ra.get("action")
        reason = ra.get("reason")

        if action == "SKIP_OPEN":
            self.skip_open_reasons[reason] += 1

        if action == "CLOSE_LONG":
            self.close_reasons[reason] += 1

        if reason == "kill_switch_active":
            self.kill_switch_events += 1

    # ============================================================
    # Rendering helpers
    # ============================================================

    def _print_header(self, title):
        print("=" * 60)
        print(title)
        print("=" * 60)

    def _print_kv(self, key, value):
        print(f"{key:30s}: {value}")

    def _print_counter(self, title, counter):
        self._print_header(title)
        if not counter:
            print("(none)")
            return
        for key, value in sorted(counter.items(), key=lambda x: (-x[1], str(x[0]))):
            print(f"{value:6d}  {str(key)}")

    # ============================================================
    # Report
    # ============================================================

    def report(self):
        self._print_header("Offline Log Summary")

        self._print_kv("meta_signal_count", self.meta_signal_count)
        self._print_kv("risk_action_count", self.risk_action_count)
        self._print_kv("kill_switch_events", self.kill_switch_events)

        self._print_counter("SKIP_OPEN reasons", self.skip_open_reasons)
        self._print_counter("CLOSE_LONG reasons", self.close_reasons)


if __name__ == "__main__":
    analyzer = OfflineLogAnalyzer("logs/offline_log.txt")
    analyzer.analyze()
    analyzer.report()
