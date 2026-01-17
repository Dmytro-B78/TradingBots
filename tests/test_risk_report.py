import csv
import subprocess
import sys

def test_risk_report_all_branches(tmp_path):
    """
    Полный тест RiskReport:
    - __init__ с кастомными файлами
    - _read_csv: файл есть / файла нет
    - generate_summary: сделки есть / сделок нет
    - модульный код __main__
    """
    from bot_ai.risk.report import RiskReport

    deny_file = tmp_path / "deny.csv"
    pass_file = tmp_path / "pass.csv"

    # --- deny.csv с одной причиной ---
    with deny_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["message"])
        writer.writeheader()
        writer.writerow({"message": "low_volume"})

    # --- pass.csv с одной сделкой ---
    with pass_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["message"])
        writer.writeheader()
        writer.writerow({"message": "ok"})

    # 1. Инициализация
    rr = RiskReport(deny_file=str(deny_file), pass_file=str(pass_file))
    assert rr.deny_file == deny_file
    assert rr.pass_file == pass_file

    # 2. _read_csv: файл есть
    denies = rr._read_csv(rr.deny_file)
    assert len(denies) == 1

    # 3. _read_csv: файла нет
    missing = rr._read_csv(tmp_path / "missing.csv")
    assert missing == []

    # 4. generate_summary: сделки есть
    summary = rr.generate_summary()
    assert summary["total_trades"] == 2
    assert summary["denies_by_reason"] == {"low_volume": 1}

    # 5. generate_summary: сделок нет
    rr_empty = RiskReport(
        deny_file=str(
            tmp_path /
            "no.csv"),
        pass_file=str(
            tmp_path /
            "no2.csv"))
    summary_empty = rr_empty.generate_summary()
    assert summary_empty["total_trades"] == 0
    assert summary_empty["success_rate_pct"] == 0

    # 6. Модульный код __main__
    result = subprocess.run(
        [sys.executable, "-m", "bot_ai.risk.report"], capture_output=True, text=True)
    assert "RiskGuard Report" in result.stdout

