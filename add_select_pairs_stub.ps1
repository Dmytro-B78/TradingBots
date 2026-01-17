# add_select_pairs_stub.ps1
# Назначение: Добавить заглушку select_pairs() в pipeline.py, если она отсутствует
# Структура:
# └── bot_ai/selector/pipeline.py

Set-Location -Path "$PSScriptRoot"

$path = ".\bot_ai\selector\pipeline.py"
$content = Get-Content $path -Raw

if ($content -notmatch "def select_pairs\(") {
    Add-Content -Encoding UTF8 $path @"

# Заглушка функции select_pairs
def select_pairs():
    print("⚠️ Заглушка: select_pairs() вызвана")
    return []
"@
    Write-Host "✅ select_pairs() добавлена в pipeline.py"
} else {
    Write-Host "ℹ️ select_pairs() уже существует в pipeline.py"
}
