# ============================================
# File: run_tests.ps1
# Назначение: Запуск тестов, проверка покрытия, CI‑режим
# Поддерживаемые режимы:
# - test     : запуск тестов + coverage + HTML + визуальный отчёт
# - coverage : только coverage + отчёты
# - ci       : режим CI (без открытия браузера)
# - clean    : удаление артефактов
# ============================================

param(
    [ValidateSet("test","coverage","ci","clean")]
    [string]$Target = "test",
    [int]$CoverageMin = 85
)

function Show-Coverage {
    if (Test-Path "coverage_reports/coverage.json") {
        $json = Get-Content coverage_reports/coverage.json | ConvertFrom-Json
        $percent = [math]::Round($json.totals.percent_covered,2)
        Write-Host ">>> Coverage: $percent% (threshold = $CoverageMin%)"
        if ($percent -lt $CoverageMin) {
            throw "Coverage below threshold: $percent% < $CoverageMin%"
        }
    } else {
        Write-Host "coverage.json not found"
    }
}

function Open-Report {
    if (Test-Path "htmlcov/index.html") {
        Start-Process "htmlcov/index.html"
        Write-Host ">>> HTML coverage report opened in browser"
    }
}

function Run-Summary {
    if (Test-Path "test_summary.py") {
        Write-Host "`n=== [TEST SUMMARY] ===`n" -ForegroundColor Cyan
        python test_summary.py
    }
}

switch ($Target) {
    "test" {
        python -m pytest --maxfail=1 --disable-warnings -q `
               --cov=bot_ai `
               --cov-fail-under=$CoverageMin `
               --cov-report=term-missing `
               --cov-report=html `
               --cov-report=json:coverage_reports/coverage.json
        Run-Summary
        Show-Coverage
        Open-Report
    }
    "coverage" {
        python -m pytest --maxfail=1 --disable-warnings -q `
               --cov=bot_ai `
               --cov-fail-under=$CoverageMin `
               --cov-report=term-missing `
               --cov-report=html `
               --cov-report=json:coverage_reports/coverage.json
        Show-Coverage
        Open-Report
    }
    "ci" {
        python -m pytest --maxfail=1 --disable-warnings -q `
               --cov=bot_ai `
               --cov-fail-under=$CoverageMin `
               --cov-report=html `
               --cov-report=json:coverage_reports/coverage.json
        Show-Coverage
        Write-Host ">>> HTML coverage report generated for CI artifact upload"
    }
    "clean" {
        Remove-Item -Recurse -Force .coverage, htmlcov, coverage_reports -ErrorAction SilentlyContinue
        Write-Host ">>> Cleaned coverage artifacts"
    }
}
