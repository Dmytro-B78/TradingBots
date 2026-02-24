param(
    [switch]$ParseOnly,
    [string]$FullLog = "logs/fff_matrix_full.log",
    [string]$FffLog = "logs/fff_matrix_fff.log",
    [string]$CsvLog  = "logs/fff_matrix_summary.csv"
)

if (-not $ParseOnly) {
    # Если не parse-only, можно добавить запуск pytest, но по новой схеме мы его не используем
    Write-Host "→ Режим полного прогона отключён. Используйте fix_pytest_ini.ps1 для запуска тестов." -ForegroundColor Yellow
    exit 0
}

# --- Парсинг свежего лога ---
if (-not (Test-Path $FullLog)) {
    Write-Host "⚠ Лог $FullLog не найден" -ForegroundColor Red
    exit 1
}

$lines = Get-Content $FullLog
$cases = @()
$current = $null

foreach ($line in $lines) {
    if ($line -match "^\[CASE\]\s*(.+)$") {
        if ($null -ne $current) { $cases += $current }
        $descLine = $Matches[1]
        $skipArgs = ""
        $expectedPass = ""
        if ($descLine -match "skip_args=(\{.*\})") { $skipArgs = $Matches[1] }
        if ($descLine -match "expected_pass=(True|False)") { $expectedPass = $Matches[1] }
        $current = [ordered]@{
            Description  = $descLine
            SkipArgs     = $skipArgs
            ExpectedPass = $expectedPass
            Logs         = @()
        }
    } elseif ($null -ne $current) {
        $current["Logs"] += $line
    }
}
if ($null -ne $current) { $cases += $current }

# --- Анализ ---
$summary = @()
foreach ($c in $cases) {
    $passed = $false
    $failed = $false
    foreach ($l in $c.Logs) {
        if ($l -match "\[FFF\]\s+прошла все фильтры") { $passed = $true }
        if ($l -match "\[FFF\]\s+не прошла фильтры")  { $failed = $true }
    }
    $spreadCut = $c.Logs -match "\[FFF\]\s+отсеян по спреду"
    $trendD1   = $c.Logs -match "\[FFF\]\s+1d SMA_fast="
    $trendLTF  = $c.Logs -match "\[FFF\]\s+1h SMA_fast="
    $result = if ($passed -and -not $failed) { "True" } elseif ($failed -and -not $passed) { "False" } else { "Неопределённо" }

    $summary += [pscustomobject]@{
        Scenario     = $c.Description
        SkipArgs     = $c.SkipArgs
        ExpectedPass = $c.ExpectedPass
        Result       = $result
        Spread       = if ($spreadCut) { "Режет" } else { "Ок/пропущен" }
        Trend_1d     = if ($trendD1) { "Есть лог" } else { "Нет" }
        Trend_1h     = if ($trendLTF) { "Есть лог" } else { "Нет" }
    }
}

# --- Вывод ---
Write-Host "→ Summary table:" -ForegroundColor Green
$summary | Format-Table -AutoSize

$totalCount = $summary.Count
if ($totalCount -gt 0) {
    $passedCount = ($summary | Where-Object { $_.Result -eq "True" }).Count
    $failedCount = ($summary | Where-Object { $_.Result -eq "False" }).Count
    $undefCount  = ($summary | Where-Object { $_.Result -eq "Неопределённо" }).Count
    $passedPct = [math]::Round(($passedCount / $totalCount) * 100, 2)
    $failedPct = [math]::Round(($failedCount / $totalCount) * 100, 2)
    $undefPct  = [math]::Round(($undefCount  / $totalCount) * 100, 2)
} else {
    $passedCount = $failedCount = $undefCount = 0
    $passedPct = $failedPct = $undefPct = 0
}

Write-Host ("→ Stats: Passed={0} ({1}%), Failed={2} ({3}%), Undefined={4} ({5}%)" -f $passedCount, $passedPct, $failedCount, $failedPct, $undefCount, $undefPct) -ForegroundColor Cyan

# --- CSV ---
$summaryRow = [pscustomobject]@{
    Scenario       = "Summary"
    SkipArgs       = "-"
    ExpectedPass   = "-"
    Result         = "-"
    Spread         = "-"
    Trend_1d       = "-"
    Trend_1h       = "-"
    PassedCount    = $passedCount
    PassedPct      = "$passedPct%"
    FailedCount    = $failedCount
    FailedPct      = "$failedPct%"
    UndefinedCount = $undefCount
    UndefinedPct   = "$undefPct%"
}
$summary + $summaryRow | Export-Csv -Path $CsvLog -Encoding UTF8 -NoTypeInformation
Write-Host "→ CSV exported to $CsvLog" -ForegroundColor Yellow
