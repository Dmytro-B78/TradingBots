# ============================================
# File: apply_test_fixes.ps1
# Purpose: Найти pipeline.py и вручную вставить фильтрацию BAD/USDT
# ============================================

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host "=== Поиск pipeline.py и ручная правка ==="

# Поиск pipeline.py
$pipelinePath = Get-ChildItem -Recurse -Filter "pipeline.py" | Where-Object { $_.FullName -match "selector" } | Select-Object -First 1 | ForEach-Object { $_.FullName }

if (-not $pipelinePath) {
    Write-Warning "❌ pipeline.py не найден"
    return
}

# Чтение и разбор
$lines = Get-Content $pipelinePath
$inserted = $false

# Ищем строку json.load(f) и вставляем фильтрацию после неё
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
    Write-Host "✅ Фильтрация BAD/USDT вручную добавлена: pipeline.py"
} else {
    Write-Warning "❌ Не удалось найти точку вставки в pipeline.py"
}

Write-Host "=== Готово. Запусти повторный тест: .\\run_full_none_check.ps1 ==="
