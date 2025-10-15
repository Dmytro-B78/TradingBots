# ------------------------------------------------------------------------------------
# FILE: run_tests.ps1
# PURPOSE: Прогон тестов и отдельный snapshot без рекурсии; мгновенная сводка.
# ------------------------------------------------------------------------------------

# Жёстко ограничиваем падения и отключаем варнинги
python -m pytest -q --disable-warnings --maxfail=5

# Запуск отдельного snapshot-раннера
python snapshot_runner.py

# Вывод статуса падений
if (Test-Path "logs/failed_tests.log") {
    Write-Host "`n=== FAILED TESTS ===" -ForegroundColor Red
    Get-Content "logs/failed_tests.log"
} else {
    Write-Host "`nВсе тесты прошли успешно" -ForegroundColor Green
}

# Вывод snapshot
if (Test-Path "project_snapshot.txt") {
    Write-Host "`n=== PROJECT SNAPSHOT ===" -ForegroundColor Cyan
    Get-Content "project_snapshot.txt"
}
