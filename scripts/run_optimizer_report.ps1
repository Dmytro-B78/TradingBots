# ================================================================
# NT-Tech Optimizer Report Runner
# ASCII-only, no Cyrillic
# ================================================================

Write-Host "Generating NT-Tech Optimizer Report..."

$env:PYTHONPATH = "C:\TradingBots\NT"

python - << 'EOF'
import json
import os
import sys

results_path = r"C:\TradingBots\NT\logs\optimizer\optimizer_results.json"
output_path = r"C:\TradingBots\NT\logs\optimizer\optimizer_report.json"

if not os.path.exists(results_path):
    print("No optimizer_results.json found. Run optimizer first.")
    sys.exit(1)

with open(results_path, "r") as f:
    results = json.load(f)

if not isinstance(results, list) or len(results) == 0:
    print("Optimizer results file is empty or invalid.")
    sys.exit(1)

# Sort by score (fallback: profit)
def score_key(x):
    return (
        x.get("score", 0),
        x.get("total_profit", 0),
        -x.get("max_drawdown_pct", 999)
    )

sorted_results = sorted(results, key=score_key, reverse=True)

top_n = sorted_results[:10]

print("Top 10 optimizer results:")
print("--------------------------")
for i, r in enumerate(top_n, 1):
    print(f"{i}. score={r.get('score', 0)} profit={r.get('total_profit', 0)} dd={r.get('max_drawdown_pct', 0)} params={r.get('params', {})}")

report = {
    "top_results": top_n,
    "total_results": len(results)
}

with open(output_path, "w") as f:
    json.dump(report, f, indent=4)

print("Optimizer report saved to:", output_path)
EOF

Write-Host "Optimizer report completed."
