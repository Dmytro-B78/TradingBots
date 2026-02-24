# 🔧 Обновление импортов: strategies → bot_ai.strategy
# 📂 Исключает .tmp, логирует каждый файл, сохраняет без BOM

$utf8 = New-Object System.Text.UTF8Encoding($false)

Get-ChildItem -Recurse -Directory | Where-Object {
    $_.FullName -notmatch '\\\.tmp$'
} | ForEach-Object {
    Get-ChildItem -Path $_.FullName -Recurse -Include *.py -File | ForEach-Object {
        Write-Host "🔄 Обработка: $($_.FullName)"
        $content = Get-Content $_.FullName -Raw
        $updated = $content -replace 'from strategies\.', 'from bot_ai.strategy.'
        [System.IO.File]::WriteAllText($_.FullName, $updated, $utf8)
    }
}
