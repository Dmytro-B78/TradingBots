# --- Запуск всех тестов ---
python -m pytest -q --disable-warnings

# --- Проверка наличия лога упавших тестов ---
if (Test-Path "logs/failed_tests.log") {
    Write-Host "`n=== FAILED TESTS ===" -ForegroundColor Red
    Get-Content "logs/failed_tests.log"
}
else {
    Write-Host "`nВсе тесты прошли успешно" -ForegroundColor Green
}

# --- Проверка наличия snapshot ---
if (Test-Path "project_snapshot.txt") {
    Write-Host "`n=== PROJECT SNAPSHOT ===" -ForegroundColor Cyan
    Get-Content "project_snapshot.txt"
}

# --- Фиксация рабочей версии в git ---
git add project_snapshot.txt
if (Test-Path "logs/failed_tests.log") {
    git add logs/failed_tests.log
}
git commit -m "fix: stable test baseline"
