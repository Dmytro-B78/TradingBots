import csv
import pytest
from bot_ai.risk.report import RiskReport

def test_generate_report_creates_csv(tmp_path):
    report_data = [
        {"pair": "BTC/USDT", "risk": 0.01, "sl": 2.0, "tp": 3.0},
        {"pair": "ETH/USDT", "risk": 0.02, "sl": 1.5, "tp": 2.5}
    ]
    output_file = tmp_path / "report.csv"
    RiskReport.generate(report_data, output_file)

    assert output_file.exists()

    with output_file.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 2
    assert rows[0]["pair"] == "BTC/USDT"
    assert rows[1]["risk"] == "0.02"

