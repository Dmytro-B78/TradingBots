# bot_ai/risk/report.py
# Модуль для анализа логов RiskGuard (risk_log.csv и risk_pass_log.csv)

import csv
from collections import Counter
from pathlib import Path
from typing import Any, Dict

class RiskReport:
    def __init__(self, deny_file: str = "risk_log.csv",
                 pass_file: str = "risk_pass_log.csv"):
        self.deny_file = Path(deny_file)
        self.pass_file = Path(pass_file)

    def generate_summary(self) -> Dict[str, Any]:
        """Читает оба CSV и возвращает сводку статистики"""
        denies = self._read_csv(self.deny_file)
        passes = self._read_csv(self.pass_file)

        total_denies = len(denies)
        total_passes = len(passes)
        total_trades = total_denies + total_passes

        reasons = [row["message"] for row in denies]
        reason_counts = Counter(reasons)

        summary = {
            "total_trades": total_trades,
            "total_passes": total_passes,
            "total_denies": total_denies,
            "success_rate_pct": (
                total_passes /
                total_trades *
                100) if total_trades > 0 else 0,
            "denies_by_reason": dict(reason_counts),
        }
        return summary

    def _read_csv(self, file_path: Path):
        if not file_path.exists():
            return []
        with file_path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

if __name__ == "__main__":
    report = RiskReport()
    summary = report.generate_summary()
    print("?? RiskGuard Report")
    print(f"Всего сделок: {summary['total_trades']}")
    print(f"Разрешено: {summary['total_passes']}")
    print(f"Отказано: {summary['total_denies']}")
    print(f"Успешность: {summary['success_rate_pct']:.2f}%")
    print("Причины отказов:")
    for reason, count in summary["denies_by_reason"].items():
        print(f" - {reason}: {count}")

