setup:
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r requirements.txt
	$(VENV_PIP) install pytest pytest-cov coverage
	$(VENV_PIP) install ruff black mypy

archive-results:
	@powershell -NoProfile -Command "$$ts = Get-Date -Format 'yyyy-MM-dd_HH-mm'; $$dst = Join-Path 'logs/archive' $$ts; New-Item -ItemType Directory -Force -Path $$dst | Out-Null; Copy-Item state\\trades_log.csv -Destination $$dst -ErrorAction SilentlyContinue; Copy-Item logs\\walk_forward*.* -Destination $$dst -ErrorAction SilentlyContinue; Copy-Item results\\*.csv -Destination $$dst -ErrorAction SilentlyContinue; Copy-Item results\\*.png -Destination $$dst -ErrorAction SilentlyContinue"
