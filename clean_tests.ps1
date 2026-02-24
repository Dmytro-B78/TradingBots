Get-ChildItem -Recurse -Path "tests" -Filter *.py | ForEach-Object {
    $file = $_.FullName
    $content = Get-Content $file -Raw -Encoding UTF8

    # Заменить "):`n    pass" на "):`r`n    pass"
    $content = $content -replace "\):`n\s*pass", "):`r`n    pass"

    # Удалить строки, содержащие только "`n    pass"
    $content = $content -replace "^\s*`n\s*pass\s*$", ""

    # Удалить строки, содержащие только "`n"
    $content = $content -replace "^\s*`n\s*$", ""

    # Удалить строки, содержащие только "`r"
    $content = $content -replace "^\s*`r\s*$", ""

    # Сохранить обратно
    Set-Content $file -Value $content -Encoding UTF8
    Write-Host "🧼 Почищено: $file" -ForegroundColor Yellow
}

Write-Host "`n✅ Все тесты очищены. Запусти .\run_all_tests.ps1 для проверки." -ForegroundColor Green
