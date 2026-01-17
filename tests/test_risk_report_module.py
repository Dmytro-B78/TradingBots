import csv

def test_risk_report_empty_and_with_data(tmp_path):
    from bot_ai.risk.report import RiskReport

    # 1. Оба файла отсутствуют > пустая статистика
    rr_empty = RiskReport(
        deny_file=tmp_path / "no_deny.csv",
        pass_file=tmp_path / "no_pass.csv"
    )
    summary_empty = rr_empty.generate_summary()
    assert summary_empty["total_trades"] == 0
    assert summary_empty["success_rate_pct"] == 0

    # 2. Файлы существуют > считаем статистику
    deny_file = tmp_path / "risk_log.csv"
    pass_file = tmp_path / "risk_pass_log.csv"

    # Заполняем deny_file
    with deny_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["message"])
        writer.writeheader()
        writer.writerow({"message": "Low volume"})
        writer.writerow({"message": "Low volume"})
        writer.writerow({"message": "High spread"})

    # Заполняем pass_file
    with pass_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["message"])
        writer.writeheader()
        writer.writerow({"message": "OK"})
        writer.writerow({"message": "OK"})

    rr_data = RiskReport(deny_file=deny_file, pass_file=pass_file)
    summary_data = rr_data.generate_summary()

    assert summary_data["total_trades"] == 5
    assert summary_data["total_passes"] == 2
    assert summary_data["total_denies"] == 3
    assert summary_data["success_rate_pct"] == 40.0
    assert summary_data["denies_by_reason"]["Low volume"] == 2
    assert summary_data["denies_by_reason"]["High spread"] == 1

