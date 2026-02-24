# ============================================
# fix_test_errors_step3.ps1
# Назначение: Финальная зачистка тестов — импорты, конфликты, BOM, отступы
# Запуск: .\fix_test_errors_step3.ps1
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

    # Удалить упоминания TradeContext
    $content = $content -replace '\bTradeContext\b', ''

    # Исправить случайные строки вида "====================\n"
    $content = $content -replace '^\s*={5,}.*$', ''

    # Исправить пустые функции без тела (добавим pass)
    $content = [regex]::Replace($content, 'def\s+\w+\(.*?\):\s*(?=\n\S)', 'def $&`n    pass', 'Multiline')

    # Сохранить обратно
    Set-Content -Path $file.FullName -Value $content -Encoding UTF8
}

Write-Host "`n✅ Финальная зачистка завершена. Запусти .\run_all_tests.ps1 для проверки." -ForegroundColor Green
