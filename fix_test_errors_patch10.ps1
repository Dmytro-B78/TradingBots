# ============================================
# fix_test_errors_patch10.ps1
# Назначение: Исправляет все конструкции вида "):`n    pass" → "):\n    pass"
# Удаляет строки, содержащие "`n    pass"
# Запуск: .\fix_test_errors_patch10.ps1
# ============================================

Get-ChildItem -Path "tests\" -Filter "*.py" -Recurse | ForEach-Object {
    Write-Host "🛠 Обработка: $($_.FullName)" -ForegroundColor Yellow

    $content = Get-Content $_.FullName -Raw -Encoding UTF8

    # Заменить все конструкции вида "):`n    pass" на "):\n    pass"
    $content = $content -replace "\):`n\s*pass", "):`r`n    pass"

    # Заменить все конструкции вида "):`npass" на "):\n    pass"
    $content = $content -replace "\):`npass", "):`r`n    pass"

    # Удалить строки, которые буквально содержат `n    pass
    $content = $content -replace "^\s*`n\s*pass\s*$", ""

    # Сохранить обратно
    Set-Content $_.FullName -Value $content -Encoding UTF8
}

Write-Host "`n✅ Все конструкции исправлены. Запусти .\run_all_tests.ps1 для проверки." -ForegroundColor Green
