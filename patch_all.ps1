# ============================================
# Patch: PositionSizer + фильтр [ERROR] + безопасный whitelist.json
# ============================================

# 1. Добавляем заглушку PositionSizer
$enginePath = Join-Path $PWD "bot_ai\\backtest\\backtest_engine.py"
$engineContent = Get-Content $enginePath -Raw
if ($engineContent -notmatch "class PositionSizer") {
    $stub = @"
# === Stub PositionSizer (auto‑added for tests) ===
class PositionSizer:
    def __init__(self, *args, **kwargs):
        pass
    def size(self, *args, **kwargs):
        return 1.0
# === End Stub ===
"@
    Add-Content -Path $enginePath -Value $stub -Encoding UTF8
    Write-Host "PositionSizer добавлен в backtest_engine.py"
} else {
    Write-Host "PositionSizer уже существует — патч не нужен"
}

# 2. Фильтр [ERROR] в pipeline.py
$pipelinePath = Join-Path $PWD "bot_ai\\selector\\pipeline.py"
$pipelineContent = Get-Content $pipelinePath -Raw
if ($pipelineContent -notmatch "\[ERROR\]") {
    Write-Warning "В pipeline.py не найдено место для фильтрации — проверь вручную"
} else {
    $patchedPipeline = $pipelineContent -replace "(top_pairs\s*=\s*\[.*\])", '$1\n# Фильтр: исключаем пары с [ERROR]\ntop_pairs = [p for p in top_pairs if "[ERROR]" not in str(p)]'
    Set-Content -Path $pipelinePath -Value $patchedPipeline -Encoding UTF8
    Write-Host "Фильтр [ERROR] добавлен в pipeline.py"
}

# 3. Безопасная работа с whitelist.json
$dataPath = Join-Path $PWD "data\\whitelist.json"
if (Test-Path $dataPath) {
    Write-Host "Создаём копию whitelist.json в temp для тестов"
    $tempWhitelist = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), "whitelist_test.json")
    Copy-Item -Path $dataPath -Destination $tempWhitelist -Force
    Write-Host "Копия создана: $tempWhitelist"
} else {
    Write-Warning "whitelist.json не найден — проверь путь"
}
