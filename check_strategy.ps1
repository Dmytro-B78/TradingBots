# ============================================
# File: check_strategy.ps1
# Purpose: Проверка стратегии mean_reversion
# Обновления:
# - Установлен ли pandas-ta
# - Импортируется ли pandas-ta
# - Рассчитан ли RSI (исправлена проверка)
# - Созданы ли CSV-файлы сделок
# ============================================

Write-Host "🔍 Проверка стратегии mean_reversion..." -ForegroundColor Cyan

# 1. Проверка наличия pandas-ta
$pandasTa = pip show pandas-ta 2>$null
if ($pandasTa) {
    Write-Host "✅ pandas-ta установлен"
} else {
    Write-Host "❌ pandas-ta не найден. Установи через: pip install pandas-ta" -ForegroundColor Red
    exit
}

# 2. Проверка импорта в файле
$code = Get-Content .\strategy\mean_reversion.py -Raw
if ($code -match "import\s+pandas_ta\s+as\s+ta") {
    Write-Host "✅ Импорт pandas-ta найден"
} else {
    Write-Host "❌ Импорт pandas-ta отсутствует в mean_reversion.py" -ForegroundColor Red
}

# 3. Проверка расчёта RSI
Write-Host "▶ Запуск стратегии..."
python main.py | Tee-Object -Variable output | Out-Null

$rsiLines = $output | Select-String "

\[DEBUG\]

 Индикаторы рассчитаны"
if ($rsiLines.Count -gt 0) {
    Write-Host "✅ RSI рассчитывается:"
    $rsiLines | ForEach-Object { Write-Host "   $_" }
} else {
    Write-Host "❌ RSI не рассчитывается. Проверь метод calculate_indicators()" -ForegroundColor Red
}

# 4. Проверка наличия CSV-файлов
$csvs = Get-ChildItem .\results\*_trades.csv -ErrorAction SilentlyContinue
if ($csvs) {
    Write-Host "✅ CSV-файлы сделок найдены:"
    $csvs | ForEach-Object { Write-Host "   $($_.Name)" }
} else {
    Write-Host "⚠️  CSV-файлы не найдены. Возможно, не было сделок." -ForegroundColor Yellow
}

Write-Host "`n✅ Проверка завершена"
