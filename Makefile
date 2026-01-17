# ============================================
# 📂 Makefile — Управление проектом
# 🧩 Поддержка: установка, тесты, отчёты, CI/CD
# ============================================

# 🔧 Переменные окружения
VENV_PYTHON = .venv/Scripts/python.exe
VENV_PIP = $(VENV_PYTHON) -m pip
TMP_DIR = .tmp

# --------------------------------------------
# 🔧 Установка и окружение
# --------------------------------------------

setup:
    @$(VENV_PIP) install --upgrade pip
    @$(VENV_PIP) install -r requirements.txt
    @$(VENV_PIP) install pytest pytest-cov coverage
    @$(VENV_PIP) install ruff black mypy

env-check:
    @make --version
    @$(VENV_PYTHON) --version
    @$(VENV_PIP) --version
    @echo pytest: && $(VENV_PYTHON) -m pytest --version
    @echo coverage: && $(VENV_PYTHON) -m coverage --version
    @echo ruff: && $(VENV_PYTHON) -m ruff --version
    @echo black: && $(VENV_PYTHON) -m black --version
    @echo mypy: && $(VENV_PYTHON) -m mypy --version

# --------------------------------------------
# 🧪 Тестирование и проверка
# --------------------------------------------

test:
    @if not exist "$(TMP_DIR)" mkdir "$(TMP_DIR)"
    @set TMP=$(TMP_DIR) && set TEMP=$(TMP_DIR) && $(VENV_PYTHON) -m pytest -v --basetemp=$(TMP_DIR)

coverage:
    @if not exist "$(TMP_DIR)" mkdir "$(TMP_DIR)"
    @set TMP=$(TMP_DIR) && set TEMP=$(TMP_DIR) && $(VENV_PYTHON) -m pytest --cov=bot_ai --cov-report=html --basetemp=$(TMP_DIR)
    @echo HTML report created in htmlcov/

publish-coverage:
    @gh-pages -d htmlcov

lint:
    @$(VENV_PYTHON) -m ruff . --fix
    @$(VENV_PYTHON) -m black .

check:
    @$(VENV_PYTHON) -m ruff . --no-fix
    @$(VENV_PYTHON) -m black --check .
    @$(VENV_PYTHON) -m mypy .

ci: clean-tmp setup check test coverage

# --------------------------------------------
# 📊 Оптимизация и визуализация
# --------------------------------------------

optimize:
    @$(VENV_PYTHON) optimize_cli.py --symbol BTCUSDT --sma-fast 10,15 --sma-slow 30,40,50 --rsi 10,15

visualize:
    @$(VENV_PYTHON) visualize_results.py

report:
    @start results\\heatmap_rsi_10.png
    @start results\\heatmap_rsi_15.png
    @type results\\best_params.csv

best:
    @type results\\best_params.csv

# --------------------------------------------
# 🪵 Логирование и архив
# --------------------------------------------

archive-logs:
    @powershell -Command " \
        $ts = Get-Date -Format 'yyyy-MM-dd_HH-mm'; \
        $dst = 'logs/archive/' + $ts; \
        New-Item -ItemType Directory -Force -Path $dst; \
        Get-ChildItem logs\\bot_live_*.log | Move-Item -Destination $dst \
    "

# --------------------------------------------
# 🧹 Очистка
# --------------------------------------------

clean-tmp:
    @if exist "$(TMP_DIR)" rmdir /s /q "$(TMP_DIR)"
    @if exist ".pytest_cache" rmdir /s /q ".pytest_cache"

clean-results:
    @if exist "results\\grid_results.csv" del /q results\\grid_results.csv
    @if exist "results\\best_params.csv" del /q results\\best_params.csv
    @if exist "results\\heatmap_rsi_10.png" del /q results\\heatmap_rsi_10.png
    @if exist "results\\heatmap_rsi_15.png" del /q results\\heatmap_rsi_15.png

# --------------------------------------------
# 🚀 Live и диагностика
# --------------------------------------------

live:
    @$(VENV_PYTHON) bot_live.py

snapshot:
    @if not exist "$(TMP_DIR)" mkdir "$(TMP_DIR)"
    @$(VENV_PYTHON) snapshot_runner.py > "$(TMP_DIR)/snapshot.log" 2>&1
    @echo Snapshot complete. See $(TMP_DIR)/snapshot.log and project_snapshot.txt

# --------------------------------------------
# 🧪 Проверка RiskGuard
# --------------------------------------------

riskguard-check:
    @$(VENV_PYTHON) -m bot_ai.tests.test_riskguard
