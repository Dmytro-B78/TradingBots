# ============================================
# fix_test_errors_patch9.ps1
# Назначение: Исправляет конструкции вида def ...():`n    pass → def ...():\n    pass
# Запуск: .\fix_test_errors_patch9.ps1
# ============================================

Get-ChildItem -Path "tests\" -Filter "*.py" -Recurse | ForEach-Object {
    Write-Host "🔧 Исправляем: $($_.FullName)" -ForegroundColor Yellow

    $content = Get-Content $_.FullName -Raw -Encoding UTF8

    # Заменить def ...():`n    pass на корректный перенос строки и отступ
    $content = $content -replace "(\bdef\s+\w+\(.*?\)):`n\s*pass", "`$1:`r`n    pass"

    # Удалить строки, которые буквально содержат `n    pass
    $content = $content -replace "^\s*`n\s*pass\s*$", ""

    # Сохранить обратно
    Set-Content $_.FullName -Value $content -Encoding UTF8
}

Write-Host "`n✅ Все конструкции def():`n    pass исправлены. Запусти .\run_all_tests.ps1 для проверки." -ForegroundColor Green
