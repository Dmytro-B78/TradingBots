# ============================================
# fix_test_errors_patch5.ps1
# Назначение: Удаляет мусорную вставку "`n    pass" и заменяет на корректный Python pass
# Запуск: .\fix_test_errors_patch5.ps1
# ============================================

Get-ChildItem -Path "tests\" -Filter "*.py" -Recurse | ForEach-Object {
    Write-Host "🧹 Чистим: $($_.FullName)" -ForegroundColor Yellow

    $content = Get-Content $_.FullName -Raw -Encoding UTF8

    # Удалить мусорную вставку `n    pass и заменить на валидный отступ
    $content = $content -replace "`n\s*pass", "    pass"

    # Сохранить обратно
    Set-Content $_.FullName -Value $content -Encoding UTF8
}

Write-Host "`n✅ Ошибочные вставки удалены. Запусти .\run_all_tests.ps1 для проверки." -ForegroundColor Green
