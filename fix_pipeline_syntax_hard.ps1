# ============================================
# File: fix_pipeline_syntax_hard.ps1
# Purpose: Удалить ошибочную \npairs строку и вставить фильтрацию как отдельную строку
# ============================================

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host "=== Жёсткая правка pipeline.py ==="

# Поиск pipeline.py
$pipelinePath = Get-ChildItem -Recurse -Filter "pipeline.py" | Where-Object { $_.FullName -match "selector" } | Select-Object -First 1 | ForEach-Object { $_.FullName }

if (-not $pipelinePath) {
    Write-Warning "❌ pipeline.py не найден"
    return
}

# Чтение строк
$lines = Get-Content $pipelinePath

# Удаление строк с \npairs = ...
$lines = $lines | Where-Object { $_ -notmatch '\\npairs\s*=' }

# Вставка фильтрации после json.load(f)
$inserted = $false
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "pairs\s*=\s*json\.load\(f\)") {
        if ($i + 1 -lt $lines.Count -and $lines[$i + 1] -match "BAD/USDT") {
            Write-Host "ℹ️ Фильтрация уже есть: pipeline.py"
            $inserted = $true
            break
        }
        $lines = $lines[0..$i] + 'pairs = [p for p in pairs if p != "BAD/USDT"]' + $lines[($i + 1)..($lines.Count - 1)]
        $inserted = $true
        break
    }
}

if ($inserted) {
    Set-Content -Path $pipelinePath -Value $lines -Encoding UTF8
    Write-Host "✅ pipeline.py очищен и фильтрация вставлена корректно"
} else {
    Write-Warning "❌ Не удалось вставить фильтрацию — точка вставки не найдена"
}

Write-Host "=== Готово. Запусти повторный тест: .\\run_full_none_check.ps1 ==="
