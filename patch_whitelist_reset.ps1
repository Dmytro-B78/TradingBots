# ============================================
# Patch: безопасный whitelist.json без симлинка
# ============================================

# Путь к боевому whitelist.json
$dataPath = Join-Path $PWD "data\\whitelist.json"

# Создаём пустой тестовый whitelist прямо в боевом файле
try {
    '[]' | Set-Content -Path $dataPath -Encoding UTF8 -Force
    Write-Host "Боевой whitelist.json заменён на пустой тестовый"
} catch {
    Write-Warning "Не удалось записать в whitelist.json — проверь, не открыт ли файл другим процессом"
}

# Проверка результата
if (Test-Path $dataPath) {
    $content = Get-Content -Path $dataPath -Raw
    Write-Host "Текущее содержимое whitelist.json:"
    Write-Host $content
} else {
    Write-Warning "Файл whitelist.json не найден — проверь путь"
}
