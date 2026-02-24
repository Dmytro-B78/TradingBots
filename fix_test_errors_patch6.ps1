# ============================================
# fix_test_errors_patch6.ps1
# Назначение: Удаляет мусорные вставки "`n    pass" и заменяет на валидный Python отступ
# Запуск: .\fix_test_errors_patch6.ps1
# ============================================

Get-ChildItem -Path "tests\" -Filter "*.py" -Recurse | ForEach-Object {
    Write-Host "🧼 Чистим: $($_.FullName)" -ForegroundColor Yellow

    $content = Get-Content $_.FullName -Raw -Encoding UTF8

    # Удалить мусорную вставку `n    pass и заменить на валидный отступ
    $content = $content -replace "`n\s*pass", "    pass"

    # Удалить строки, которые состоят только из `n    pass
    $content = $content -replace "^\s*`n\s*pass\s*$", ""

    # Сохранить обратно
    Set-Content $_.FullName -Value $content -Encoding UTF8
}

Write-Host "`n✅ Мусор удалён. Запусти .\run_all_tests.ps1 для проверки." -ForegroundColor Green
