# ============================================
# File: run_full_none_check.ps1
# Purpose: Запуск полного тестового пакета с поиском ожиданий None
#          Под PowerShell 7, без NativeCommandError, с логом в UTF-8
# ============================================

$ErrorActionPreference = "Stop"
Write-Host "=== Запуск полного тестового пакета с поиском ожиданий None ==="

# 1. Проверка BOM
$pytestIniPath = Join-Path $PWD "pytest.ini"
if (Test-Path $pytestIniPath) {
    $bom = Get-Content $pytestIniPath -Encoding Byte -TotalCount 3
    if ($bom[0] -eq 0xEF -and $bom[1] -eq 0xBB -and $bom[2] -eq 0xBF) {
        Write-Host "BOM обнаружен."
    } else {
        Write-Host "BOM не обнаружен."
    }
} else {
    Write-Warning "pytest.ini не найден"
}

# 2. Запуск pytest через cmd /c (stderr → stdout, без NativeCommandError)
Write-Host "=== Запуск pytest ==="
$pythonPath = Join-Path $PWD ".venv\\Scripts\\python.exe"
$pytestOutput = cmd /c "`"$pythonPath`" -m pytest tests -vv --disable-warnings --maxfail=0 2>&1"
$logPath = Join-Path $PWD "full_test_log.txt"
$pytestOutput | Set-Content -Path $logPath -Encoding UTF8

# 3. Анализ 'is None'
Write-Host "=== Проверки 'is None' ==="
if ($pytestOutput -match "is None") {
    ($pytestOutput -split "`r?`n") | Where-Object { $_ -match "is None" } | ForEach-Object { Write-Host $_ }
} else {
    Write-Host "Нет проверок 'is None'."
}

# 4. Анализ ошибок ERROR
Write-Host "=== Ошибки ERROR ==="
$errors = ($pytestOutput -split "`r?`n") | Where-Object { $_ -match "ERROR" }
if ($errors) {
    Write-Host "Найдено $($errors.Count) ошибок:"
    $errors | ForEach-Object { Write-Host $_ }
} else {
    Write-Host "Ошибок нет."
}

# 5. Анализ упавших тестов
Write-Host "=== FAILED тесты ==="
$failed = ($pytestOutput -split "`r?`n") | Where-Object { $_ -match "FAILED" }
if ($failed) {
    $failed | ForEach-Object { Write-Host $_ }
} else {
    Write-Host "Нет упавших тестов."
}

Write-Host "=== Анализ завершён. Лог: $logPath ==="
