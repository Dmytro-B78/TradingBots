# ============================================
# Patch: использование temp‑whitelist вместо боевого
# ============================================

# Путь к временной копии
$tempWhitelist = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), "whitelist_test.json")

# Создаём пустой тестовый whitelist
'[]' | Set-Content -Path $tempWhitelist -Encoding UTF8 -Force
Write-Host "Создан тестовый whitelist: $tempWhitelist"

# Устанавливаем переменную окружения для Python/pytest
# Пусть код читает путь из переменной WHITELIST_PATH
[System.Environment]::SetEnvironmentVariable("WHITELIST_PATH", $tempWhitelist, "Process")
Write-Host "Переменная окружения WHITELIST_PATH установлена на temp‑файл"

# Проверка
Write-Host "Теперь тесты должны использовать: $env:WHITELIST_PATH"
