import csv

def test_risk_report_empty_and_with_data(tmp_path):
    from bot_ai.risk.report import RiskReport

    # 1. Р В Р’В Р РЋРІР‚С”Р В Р’В Р вЂ™Р’В±Р В Р’В Р вЂ™Р’В° Р В Р Р‹Р Р†Р вЂљРЎвЂєР В Р’В Р вЂ™Р’В°Р В Р’В Р Р†РІР‚С›РІР‚вЂњР В Р’В Р вЂ™Р’В»Р В Р’В Р вЂ™Р’В° Р В Р’В Р РЋРІР‚СћР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р Р‹Р В РЎвЂњР В Р Р‹Р РЋРІР‚СљР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р В РІР‚В Р В Р Р‹Р РЋРІР‚СљР В Р Р‹Р В РІР‚в„–Р В Р Р‹Р Р†Р вЂљРЎв„ў > Р В Р’В Р РЋРІР‚вЂќР В Р Р‹Р РЋРІР‚СљР В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В°Р В Р Р‹Р В Р РЏ Р В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В°Р В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р РЋРІР‚ВР В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р РЋРІР‚ВР В Р’В Р РЋРІР‚СњР В Р’В Р вЂ™Р’В°
    rr_empty = RiskReport(
        deny_file=tmp_path / "no_deny.csv",
        pass_file=tmp_path / "no_pass.csv"
    )
    summary_empty = rr_empty.generate_summary()
    assert summary_empty["total_trades"] == 0
    assert summary_empty["success_rate_pct"] == 0

    # 2. Р В Р’В Р вЂ™Р’В¤Р В Р’В Р вЂ™Р’В°Р В Р’В Р Р†РІР‚С›РІР‚вЂњР В Р’В Р вЂ™Р’В»Р В Р Р‹Р Р†Р вЂљРІвЂћвЂ“ Р В Р Р‹Р В РЎвЂњР В Р Р‹Р РЋРІР‚СљР В Р Р‹Р Р†Р вЂљР’В°Р В Р’В Р вЂ™Р’ВµР В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р В РІР‚В Р В Р Р‹Р РЋРІР‚СљР В Р Р‹Р В РІР‚в„–Р В Р Р‹Р Р†Р вЂљРЎв„ў > Р В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљР Р‹Р В Р’В Р РЋРІР‚ВР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В°Р В Р’В Р вЂ™Р’ВµР В Р’В Р РЋР’В Р В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В°Р В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р РЋРІР‚ВР В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р РЋРІР‚ВР В Р’В Р РЋРІР‚СњР В Р Р‹Р РЋРІР‚Сљ
    deny_file = tmp_path / "risk_log.csv"
    pass_file = tmp_path / "risk_pass_log.csv"

    # Р В Р’В Р Р†Р вЂљРІР‚СњР В Р’В Р вЂ™Р’В°Р В Р’В Р РЋРІР‚вЂќР В Р’В Р РЋРІР‚СћР В Р’В Р вЂ™Р’В»Р В Р’В Р В РІР‚В¦Р В Р Р‹Р В Р РЏР В Р’В Р вЂ™Р’ВµР В Р’В Р РЋР’В deny_file
    with deny_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["message"])
        writer.writeheader()
        writer.writerow({"message": "Low volume"})
        writer.writerow({"message": "Low volume"})
        writer.writerow({"message": "High spread"})

    # Р В Р’В Р Р†Р вЂљРІР‚СњР В Р’В Р вЂ™Р’В°Р В Р’В Р РЋРІР‚вЂќР В Р’В Р РЋРІР‚СћР В Р’В Р вЂ™Р’В»Р В Р’В Р В РІР‚В¦Р В Р Р‹Р В Р РЏР В Р’В Р вЂ™Р’ВµР В Р’В Р РЋР’В pass_file
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


