# ============================================
# fix_test_errors_step2.ps1
# Назначение: Исправляет импорты RiskGuard, удаляет TradeContext, чистит Git-конфликты и BOM
# Запуск: .\fix_test_errors_step2.ps1
# ============================================

$files = Get-ChildItem -Path "tests\" -Filter "*.py" -Recurse

foreach ($file in $files) {
    Write-Host "🛠 Обработка: $($file.FullName)" -ForegroundColor Yellow

    $content = Get-Content $file.FullName -Raw -Encoding UTF8

    # Удаление BOM
    $content = $content -replace "^\uFEFF", ""

    # Удаление конфликтных маркеров Git
    $content = [regex]::Replace($content, '<<<<<<<.*?=======', '', 'Singleline')
    $content = [regex]::Replace($content, '>>>>>>>.*', '', 'Singleline')

    # Заменить импорт RiskGuard + TradeContext
    $content = $content -replace 'from bot_ai\.risk\.risk_guard import RiskGuard, TradeContext', 'from bot_ai.risk.risk_guard import RiskGuardWithLogging as RiskGuard'

    # Удалить импорт только TradeContext
    $content = $content -replace 'from bot_ai\.risk\.risk_guard import TradeContext', ''

    # Удалить упоминания TradeContext, если остались
    $content = $content -replace '\bTradeContext\b', ''

    # Сохранить обратно
    Set-Content -Path $file.FullName -Value $content -Encoding UTF8
}

Write-Host "`n✅ Исправления завершены. Запусти .\run_all_tests.ps1 для проверки." -ForegroundColor Green
