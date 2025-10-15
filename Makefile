# Makefile for NeuroTrade (ASCII, tabs only)

VENV_PYTHON := $(CURDIR)/.venv/Scripts/python.exe
VENV_PIP := "$(VENV_PYTHON)" -m pip
TMP_DIR := $(CURDIR)/.tmp

clean-tmp:
	@if exist "$(TMP_DIR)" rmdir /s /q "$(TMP_DIR)"
	@if exist ".pytest_cache" rmdir /s /q ".pytest_cache"

setup:
	@echo "=== Installing Python dependencies into .venv ==="
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install pytest pytest-cov coverage
	@echo "=== Setup complete ==="

test:
	set TMP=$(TMP_DIR) && set TEMP=$(TMP_DIR) && "$(VENV_PYTHON)" -m pytest -v --basetemp=$(TMP_DIR)

coverage:
	set TMP=$(TMP_DIR) && set TEMP=$(TMP_DIR) && "$(VENV_PYTHON)" -m pytest --cov=bot_ai --cov-report=html --basetemp=$(TMP_DIR)
	@echo HTML report created in htmlcov/

publish-coverage:
	gh-pages -d htmlcov

ci: clean-tmp setup test coverage

env-check:
	@echo "=== Environment check ==="
	@make --version
	@"$(VENV_PYTHON)" --version
	@$(VENV_PIP) --version
	@echo "pytest: " && "$(VENV_PYTHON)" -m pytest --version
	@echo "coverage: " && "$(VENV_PYTHON)" -m coverage --version
