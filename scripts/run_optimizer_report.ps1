# ================================================================
# NT-Tech Optimizer Report Runner
# ASCII-only, no Cyrillic
# ================================================================

Write-Host "Generating NT-Tech Optimizer Report..."

$env:PYTHONPATH = "C:\TradingBots\NT"

python - << "EOF"
from bot_ai.engine.optimizer_report import OptimizerReport
import json
import os

results_path = r"C:\TradingBots\NT\bot_ai\results\optimizer_results.json"
output_path = r"C:\TradingBots\NT\bot_ai\results\optimizer_report.json"

if not os.path.exists(results_path):
    print("No optimizer_results.json found. Run optimizer first.")
    exit(1)

with open(results_path, "r") as f:
    results = json.load(f)

report = OptimizerReport(results, output_path)
report.print_top(10)
report.save()
EOF

Write-Host "Optimizer report completed."
