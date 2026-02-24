# ============================================
# fix_test_errors_patch7.ps1
# Назначение: Удаляет строки, содержащие "`n    pass" — мусор от PowerShell
# Запуск: .\fix_test_errors_patch7.ps1
# ============================================

Get-ChildItem -Path "tests\" -Filter "*.py" -Recurse | ForEach-Object {
    Write-Host "🧹 Удаляем мусор в: $($_.FullName)" -ForegroundColor Yellow

    $lines = Get-Content $_.FullName -Encoding UTF8

    # Удалить строки, содержащие `n    pass
    $cleaned = $lines | Where-Object { $_ -notmatch "`n\s*pass" }

    # Сохранить обратно
    Set-Content $_.FullName -Value $cleaned -Encoding UTF8
}

Write-Host "`n✅ Строки с '`n    pass' удалены. Запусти .\run_all_tests.ps1 для проверки." -ForegroundColor Green
