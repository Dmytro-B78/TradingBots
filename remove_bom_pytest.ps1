Write-Host "=== Удаляем BOM из pytest.ini ==="
$content = Get-Content pytest.ini
Set-Content -Path pytest.ini -Value $content -Encoding UTF8
Write-Host "pytest.ini сохранён без BOM."
