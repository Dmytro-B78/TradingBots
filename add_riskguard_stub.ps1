# ============================================
# Patch: Добавление заглушки RiskGuard в backtest_engine.py
# ============================================

$enginePath = Join-Path $PWD "bot_ai\\backtest\\backtest_engine.py"

# Читаем текущий файл
$engineContent = Get-Content $enginePath -Raw

# Проверяем, есть ли уже RiskGuard
if ($engineContent -notmatch "class RiskGuard") {
    $stub = @"
# === Stub RiskGuard (auto‑added for tests) ===
class RiskGuard:
    def __init__(self, *args, **kwargs):
        pass
    def check(self, *args, **kwargs):
        return True
# === End Stub ===
"@

    # Добавляем в конец файла
    Add-Content -Path $enginePath -Value $stub -Encoding UTF8
    Write-Host "Заглушка RiskGuard добавлена в backtest_engine.py"
} else {
    Write-Host "RiskGuard уже существует — патч не нужен"
}
