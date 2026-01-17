# ============================================
# Patch: безопасный whitelist.json через симлинк
# ============================================

# Путь к боевому whitelist.json
$dataPath = Join-Path $PWD "data\\whitelist.json"

# Путь к временной копии
$tempWhitelist = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), "whitelist_test.json")

# Создаём пустой тестовый whitelist
'[]' | Set-Content -Path $tempWhitelist -Encoding UTF8
Write-Host "Создан тестовый whitelist: $tempWhitelist"

# Удаляем боевой файл, если он существует
if (Test-Path $dataPath) {
    try {
        Remove-Item -Path $dataPath -Force
        Write-Host "Удалён боевой whitelist.json"
    } catch {
        Write-Warning "Не удалось удалить боевой whitelist.json — возможно, он уже удалён или заблокирован"
    }
}

# Создаём симлинк на temp‑файл
try {
    New-Item -ItemType SymbolicLink -Path $dataPath -Target $tempWhitelist -Force
    Write-Host "Симлинк создан: $dataPath → $tempWhitelist"
} catch {
    Write-Warning "Не удалось создать симлинк — проверь права администратора"
}
