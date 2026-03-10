# ============================================
# File: C:\TradingBots\NT\bot_ai\risk\risk_report.py
# Purpose: Minimal RiskReport implementation required by tests
# Encoding: UTF-8 without BOM
# ============================================

import pandas as pd

class RiskReport:
    @staticmethod
    def generate(data, output_file):
        """
        Create a CSV report from a list of dicts.
        Required by tests/test_risk_report.py
        """
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
