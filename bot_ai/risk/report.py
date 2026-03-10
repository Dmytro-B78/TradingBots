import csv
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List
import pandas as pd


class RiskReport:
    """
    Original RiskGuard summary report + CSV generator required by tests.
    """

    def __init__(self, deny_file: str = "risk_log.csv",
                 pass_file: str = "risk_pass_log.csv"):
        self.deny_file = Path(deny_file)
        self.pass_file = Path(pass_file)

    # === NEW METHOD REQUIRED BY TESTS ===
    @staticmethod
    def generate(data, output_file):
        """
        Create a CSV report from a list of dicts.
        Required by tests/test_risk_report.py
        """
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)

    # === ORIGINAL LOGIC (leave unchanged) ===
    def _read_csv(self, file_path: Path) -> List[Dict[str, Any]]:
        if not file_path.exists():
            return []
        with file_path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def generate_summary(self) -> Dict[str, Any]:
        denies = self._read_csv(self.deny_file)
        passes = self._read_csv(self.pass_file)

        total_denies = len(denies)
        total_passes = len(passes)
        total_trades = total_denies + total_passes

        reasons = [row.get("message", "Unknown") for row in denies]
        reason_counts = Counter(reasons)

        return {
            "total_trades": total_trades,
            "total_passes": total_passes,
            "total_denies": total_denies,
            "success_rate_pct": (
                total_passes / total_trades * 100 if total_trades > 0 else 0
            ),
            "denies_by_reason": dict(reason_counts),
        }
