# =========================
# NeuroTrade Unified Test Runner
# =========================
# Запуск тестов с проверкой покрытия кода и обработкой пустого ключа в coverage.json

param(
    [string]$Target = "local",   # Режим запуска: local или ci
    [int]$CoverageMin = 85       # Минимальный процент покрытия
)

Write-Host "=== NeuroTrade Test Runner ==="
Write-Host "Режим: $Target"
Write-Host "Минимальное покрытие: $CoverageMin%"

# 1. Проверка наличия pytest-cov
Write-Host "Проверяю наличие pytest-cov..."
python -m pip show pytest-cov > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Устанавливаю pytest и pytest-cov..."
    python -m pip install pytest pytest-cov
}

# 2. Запуск pytest с ковереджем
Write-Host "=== DEBUG: запускаю pytest с подробным выводом ==="
$pytestCmd = "python -m pytest tests -vv --maxfail=1 --disable-warnings --cov=bot_ai --cov-report=html --cov-report=json:coverage_reports/coverage.json"
Write-Host "Команда: $pytestCmd"
Invoke-Expression $pytestCmd

Write-Host "=== DEBUG: pytest завершил работу ==="

# 3. Проверка наличия coverage.json
if (-Not (Test-Path "coverage_reports/coverage.json")) {
    Write-Warning "⚠ coverage.json не найден — пропускаю проверку"
    exit 1
}

# 4. Чтение coverage.json с обработкой пустого ключа
try {
    $json = Get-Content coverage_reports/coverage.json | ConvertFrom-Json -AsHashTable
    if ($json.ContainsKey("")) {
        Write-Host "Удаляю пустой ключ из coverage.json..."
        $json.Remove("")
    }
} catch {
    Write-Error "Ошибка чтения coverage.json: $_"
    exit 1
}

# 5. Извлечение процента покрытия
if ($json.ContainsKey("totals")) {
    $coverage = [math]::Round($json["totals"]["percent_covered"], 2)
    Write-Host "Покрытие кода: $coverage%"
    if ($coverage -lt $CoverageMin) {
        Write-Error "Покрытие ниже минимального порога ($CoverageMin%)"
        exit 1
    }
} else {
    Write-Error "Не найден ключ 'totals' в coverage.json"
    exit 1
}

Write-Host "✅ Все проверки пройдены"
exit 0
