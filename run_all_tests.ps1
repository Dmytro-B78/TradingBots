# ============================================
# run_all_tests.ps1
# Назначение: Запуск всех тестов проекта с покрытием
# Использует: pytest + pytest-cov
# Расположение: корень проекта (C:\TradingBots\NT)
# Запуск: .\run_all_tests.ps1
# ============================================

Write-Host "🚀 Запуск всех тестов проекта..." -ForegroundColor Cyan

# Шаг 1: Активируем виртуальное окружение, если неактивно
if (-not $env:VIRTUAL_ENV) {
    & .\.venv\Scripts\Activate.ps1
}

# Шаг 2: Запускаем pytest с покрытием
python -m pytest tests/ `
    --cov=bot_ai `
    --cov-report=term-missing `
    -v

# Шаг 3: Завершение
Write-Host "`n✅ Все тесты завершены." -ForegroundColor Green
