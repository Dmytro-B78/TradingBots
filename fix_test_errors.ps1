# ============================================
# fix_test_errors.ps1
# Назначение: Исправляет импорты, Git-конфликты и BOM в тестах
# Запуск: .\fix_test_errors.ps1
# ============================================

$files = @(
    "tests/test_position_sizer_sl.py",
    "tests/test_project_state.py",
    "tests/test_risk_guard.py",
    "tests/test_risk_guard_extended.py",
    "tests/test_risk_guard_logging.py",
    "tests/test_risk_report.py",
    "tests/test_riskguard.py",
    "tests/test_riskguard_block_cooldown.py",
    "tests/test_riskguard_block_daily_loss.py",
    "tests/test_riskguard_block_kill_switch.py",
    "tests/test_riskguard_block_logging.py",
    "tests/test_riskguard_block_low_volume.py",
    "tests/test_riskguard_block_max_positions.py",
    "tests/test_riskguard_block_pass.py",
    "tests/test_riskguard_block_position_size.py",
    "tests/test_riskguard_block_risk_per_trade.py",
    "tests/test_riskguard_block_spread.py",
    "tests/test_riskguard_block_total_loss.py",
    "tests/test_sl_tp.py",
    "tests/test_smoke.py"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "🛠 Обработка: $file" -ForegroundColor Yellow

        # Чтение содержимого
        $content = Get-Content $file -Raw -Encoding UTF8

        # Удаление BOM (U+FEFF)
        $content = $content -replace "^\uFEFF", ""

        # Удаление конфликтных маркеров Git
        $content = [regex]::Replace($content, '<<<<<<<.*?=======', '', 'Singleline')
        $content = [regex]::Replace($content, '>>>>>>>.*', '', 'Singleline')

        # Исправление импорта: exec → execution
        $content = $content -replace 'from bot_ai\.exec\.', 'from bot_ai.execution.'

        # Сохранение обратно
        Set-Content -Path $file -Value $content -Encoding UTF8
    } else {
        Write-Host "⚠️ Файл не найден: $file" -ForegroundColor DarkGray
    }
}

Write-Host "`n✅ Исправления завершены. Запусти .\run_all_tests.ps1 для проверки." -ForegroundColor Green
