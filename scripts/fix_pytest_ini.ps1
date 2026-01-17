# scripts/fix_pytest_ini.ps1
# Добавлены annotationlib, argmax, array, array_interface_testing, ast, atexit, axolotl_curve25519, backports в $exclude.

param(
    [switch]$PushPages
)

Write-Host "=== FFF Matrix: подготовка окружения ===" -ForegroundColor Cyan

Write-Host "Очищаем старые pytest-of-* директории..." -ForegroundColor Yellow
Get-ChildItem "$env:TEMP" -Directory -Filter "pytest-of-*" -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "Генерируем requirements.txt..." -ForegroundColor Yellow
$projectRoot = "C:\TradingBots\NT"
$outputFile = Join-Path $projectRoot "requirements.txt"

$stdlib = @(
    "builtins","__builtin__","__main__","__future__","__pypy__","abc",
    "sys","os","re","math","json","datetime","pathlib","logging","typing",
    "functools","itertools","collections","subprocess","shutil","argparse",
    "unittest","uuid","random","statistics","decimal","fractions","enum",
    "dataclasses","inspect","threading","asyncio","time","email","http",
    "urllib","xml","html","glob","hashlib","base64","copy","traceback"
)
$exclude = @(
    "all","any","true","false","test","tests",
    "an","and","or","not","android",
    "annotationlib","argmax","array","array_interface_testing","ast","atexit","axolotl_curve25519","backports"
)

$imports = Get-ChildItem -Path $projectRoot -Recurse -Include *.py |
    Select-String -Pattern '^\s*(import|from)\s+([a-zA-Z0-9_\.]+)' |
    ForEach-Object {
        $_.Matches[0].Groups[2].Value.Split('.')[0]
    } |
    Where-Object {
        $_ -and
        ($stdlib -notcontains $_) -and
        ($exclude -notcontains $_) -and
        ($_ -notmatch '^_') -and
        ($_ -notmatch '^__') -and
        ($_ -notmatch '^[0-9]+$') -and
        ($_ -notmatch '^[a-zA-Z]$')
    } |
    Sort-Object -Unique

Write-Host "Найдено внешних пакетов: $($imports.Count)" -ForegroundColor Green
$imports | Set-Content -Path $outputFile -Encoding UTF8
Write-Host "requirements.txt создан: $outputFile" -ForegroundColor Green

Write-Host "Устанавливаем зависимости..." -ForegroundColor Cyan
pip install -r $outputFile

Write-Host "=== FFF Matrix: запуск тестов ===" -ForegroundColor Cyan
pytest --maxfail=1 --disable-warnings --basetemp C:\Temp -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Тесты завершились с ошибкой" -ForegroundColor Red
}

# Остальная часть скрипта без изменений...
