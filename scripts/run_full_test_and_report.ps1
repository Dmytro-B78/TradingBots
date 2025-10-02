# scripts/run_full_test_and_report.ps1
# ------------------------------------------------------------
# Назначение:
# 1. Запустить скрипт generate_test_report.py
# 2. Вывести краткий результат тестов в консоль
# 3. Открыть HTML-отчёт в браузере
# ------------------------------------------------------------

# Шаг 1 — Запуск скрипта генерации отчёта
Write-Host "Запускаю тесты и генерацию отчёта..." -ForegroundColor Cyan
python scripts/generate_test_report.py

# Шаг 2 — Вывод краткого содержимого changes.log (последние 10 строк)
Write-Host "`nПоследние записи changes.log:" -ForegroundColor Cyan
Get-Content changes.log -Tail 10

# Шаг 3 — Открытие HTML-отчёта в браузере
$reportPath = Join-Path (Get-Location) "htmlcov/index.html"
if (Test-Path $reportPath) {
    Write-Host "`nОткрываю HTML-отчёт..." -ForegroundColor Cyan
    Start-Process $reportPath
} else {
    Write-Host "`nHTML-отчёт не найден. Проверьте, что pytest с --cov-report=html отработал корректно." -ForegroundColor Red
}
