# tests/test_risk_report.py
# Проверка работы RiskReport: подсчёт сделок, отказов и причин

import csv
from bot_ai.risk.report import RiskReport


def test_risk_report_summary(tmp_path):
    deny_file = tmp_path / "risk_log.csv"
    pass_file = tmp_path / "risk_pass_log.csv"

    # Создаём фейковые логи
    with deny_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "message"])
        writer.writerow(["2025-09-21T10:00:00", "Объём слишком мал"])
        writer.writerow(["2025-09-21T11:00:00", "Объём слишком мал"])
        writer.writerow(["2025-09-21T12:00:00", "Кулдаун"])

    with pass_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "message"])
        writer.writerow(["2025-09-21T10:05:00", "Сделка разрешена ✅"])
        writer.writerow(["2025-09-21T11:15:00", "Сделка разрешена ✅"])

    report = RiskReport(deny_file, pass_file)
    summary = report.generate_summary()

    assert summary["total_trades"] == 5
    assert summary["total_passes"] == 2
    assert summary["total_denies"] == 3
    assert summary["success_rate_pct"] == 40.0
    assert summary["denies_by_reason"]["Объём слишком мал"] == 2
    assert summary["denies_by_reason"]["Кулдаун"] == 1
