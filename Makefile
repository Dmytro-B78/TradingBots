# Makefile для NeuroTrade — установка зависимостей, тесты, отчёт покрытия, CI
# Всегда используем Python из локального .venv и отдельную temp-папку

VENV_PYTHON := $(CURDIR)/.venv/Scripts/python.exe
VENV_PIP := "$(VENV_PYTHON)" -m pip
TMP_DIR := $(CURDIR)/.tmp

# Очистка временных директорий
clean-tmp:
	if exist "$(TMP_DIR)" rmdir /s /q "$(TMP_DIR)"
	if exist ".pytest_cache" rmdir /s /q ".pytest_cache"

# Установка зависимостей
setup:
	@echo "=== Установка Python-зависимостей в .venv ==="
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install pytest pytest-cov coverage
	@echo "=== Установка завершена ==="

# Запуск тестов (с отдельным TMP/TEMP и --basetemp)
test:
	set TMP=$(TMP_DIR) && set TEMP=$(TMP_DIR) && "$(VENV_PYTHON)" -m pytest -v --basetemp=$(TMP_DIR)

# Генерация отчёта покрытия
coverage:
	set TMP=$(TMP_DIR) && set TEMP=$(TMP_DIR) && "$(VENV_PYTHON)" -m pytest --cov=bot_ai --cov-report=html --basetemp=$(TMP_DIR)
	@echo HTML-отчёт создан в папке htmlcov

# Публикация отчёта на GitHub Pages
publish-coverage:
	gh-pages -d htmlcov

# Полный цикл для CI/CD
ci: clean-tmp setup test coverage

# Проверка окружения
env-check:
	@echo "=== Проверка окружения ==="
	@make --version
	@"$(VENV_PYTHON)" --version
	@$(VENV_PIP) --version
	@echo "pytest: " && "$(VENV_PYTHON)" -m pytest --version
	@echo "coverage: " && "$(VENV_PYTHON)" -m coverage --version