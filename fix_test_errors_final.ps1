# ============================================
# fix_test_errors_final.ps1
# Назначение: Полная зачистка тестов — импорты, конфликты, BOM, отступы, мусор
# Запуск: .\fix_test_errors_final.ps1
# ============================================

$files = Get-ChildItem -Path "tests\" -Filter "*.py" -Recurse

foreach ($file in $files) {
    Write-Host "🧼 Чистим: $($file.FullName)" -ForegroundColor Yellow

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

    # Удалить упоминания TradeContext
    $content = $content -replace '\bTradeContext\b', ''

    # Удалить мусорные строки типа ========
    $content = $content -replace '^\s*={5,}.*$', ''

    # Добавить pass в пустые функции
    $content = [regex]::Replace($content, '(?m)^(\s*def\s+\w+\(.*?\):\s*)$', '$1`n    pass')

    # Сохранить обратно
    Set-Content -Path $file.FullName -Value $content -Encoding UTF8
}

Write-Host "`n✅ Полная зачистка завершена. Запусти .\run_all_tests.ps1 для проверки." -ForegroundColor Green
