# ============================================
# fix_pass_lines.ps1
# Назначение: Исправляет строки вида "):`n    pass" и удаляет "`n    pass"
# Запуск: .\fix_pass_lines.ps1
# ============================================

Get-ChildItem -Path "tests\" -Filter "*.py" -Recurse | ForEach-Object {
    Write-Host "🧼 Чистим: $($_.FullName)" -ForegroundColor Yellow

    $content = Get-Content $_.FullName -Raw -Encoding UTF8

    # Исправить конструкции вида "):`n    pass" → "):\n    pass"
    $content = $content -replace "\):`n\s*pass", "):`r`n    pass"

    # Удалить строки, содержащие только "`n    pass"
    $content = $content -replace "^\s*`n\s*pass\s*$", ""

    # Удалить строки, содержащие только "`n"
    $content = $content -replace "^\s*`n\s*$", ""

    # Сохранить обратно
    Set-Content $_.FullName -Value $content -Encoding UTF8
}

Write-Host "`n✅ Все мусорные вставки удалены. Запусти .\run_all_tests.ps1 для проверки." -ForegroundColor Green
