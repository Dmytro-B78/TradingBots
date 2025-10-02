# run_tests.ps1
# ------------------------------------------------------------
# Универсальный скрипт для локального и CI-прогона тестов NeuroTrade.
# ------------------------------------------------------------
# Параметры:
# -Target       : режим запуска ("ci" или "local")
# -CoverageMin  : минимальный процент покрытия для успешного прогона
# ------------------------------------------------------------

param(
    [string]$Target = "local",
    [int]$CoverageMin = 85
)

Write-Host "=== NeuroTrade Test Runner ===" -ForegroundColor Cyan
Write-Host "Режим: $Target" -ForegroundColor Yellow
Write-Host "Минимальное покрытие: $CoverageMin%" -ForegroundColor Yellow

# Шаг 1 — Активация виртуального окружения, если есть
if (Test-Path ".venv/Scripts/Activate.ps1") {
    Write-Host "Активирую виртуальное окружение..." -ForegroundColor Cyan
    . .\.venv\Scripts\Activate.ps1
}

# Шаг 2 — Проверка и установка pytest-cov в текущем окружении
Write-Host "Проверяю наличие pytest-cov..." -ForegroundColor Cyan
python -m pip show pytest-cov | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "pytest-cov не найден — устанавливаю..." -ForegroundColor Yellow
    python -m pip install pytest-cov
}

# Шаг 3 — Создаём папку для отчётов покрытия
if (-Not (Test-Path coverage_reports)) {
    New-Item -ItemType Directory -Path coverage_reports | Out-Null
}

# Шаг 4 — Задаём свой temp-каталог для pytest
$env:PYTEST_ADDOPTS = "--basetemp=./.pytest_temp"

# Шаг 5 — Добавляем корень проекта в PYTHONPATH
$env:PYTHONPATH = "$PWD"

# Шаг 6 — Запуск тестов из папки tests с подробным выводом
Write-Host "=== DEBUG: запускаю pytest с подробным выводом ===" -ForegroundColor Magenta
$pytestCmd = "python -m pytest tests -vv --maxfail=1 --disable-warnings --cov=. --cov-report=html --cov-report=json:coverage_reports/coverage.json"
Write-Host "Команда: $pytestCmd" -ForegroundColor Magenta
$pytestResult = Invoke-Expression $pytestCmd
Write-Host "=== DEBUG: pytest завершил работу ===" -ForegroundColor Magenta

# Шаг 7 — Проверка покрытия
if (Test-Path "coverage_reports/coverage.json") {
    $json = Get-Content coverage_reports/coverage.json | ConvertFrom-Json
    $percent = [math]::Round($json.totals.percent_covered, 2)
    Write-Host "Покрытие кода: $percent%" -ForegroundColor Cyan

    if ($percent -lt $CoverageMin) {
        Write-Host "❌ Покрытие ниже порога ($CoverageMin%)" -ForegroundColor Red
        $status = "FAIL"
        if ($Target -eq "ci") { exit 1 }
    } else {
        Write-Host "✅ Покрытие соответствует порогу" -ForegroundColor Green
        $status = "PASS"
    }
} else {
    Write-Host "⚠ coverage.json не найден — пропускаю проверку" -ForegroundColor Yellow
    $status = "UNKNOWN"
    if ($Target -eq "ci") { exit 1 }
}

# Шаг 8 — Логирование результата
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$logEntry = "$timestamp — Target=$Target — CoverageMin=$CoverageMin — Status=$status`n$pytestResult`n"
Add-Content -Path changes.log -Value $logEntry -Encoding UTF8

Write-Host "Лог обновлён: changes.log" -ForegroundColor Cyan
Write-Host "HTML-отчёт: htmlcov/index.html" -ForegroundColor Cyan
