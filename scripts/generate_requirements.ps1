# generate_requirements.ps1
# Автоматическая генерация requirements.txt из импортов проекта

$projectRoot = "C:\TradingBots\NT"
$outputFile = Join-Path $projectRoot "requirements.txt"

# Список стандартных модулей Python (минимальный, можно расширить)
$stdlib = @(
    "sys","os","re","math","json","datetime","pathlib","logging","typing",
    "functools","itertools","collections","subprocess","shutil","argparse",
    "unittest","uuid","random","statistics","decimal","fractions","enum",
    "dataclasses","inspect","threading","asyncio","time","email","http",
    "urllib","xml","html","glob","hashlib","base64","copy","traceback"
)

Write-Host "Сканируем проект для поиска импортов..." -ForegroundColor Cyan

$imports = Get-ChildItem -Path $projectRoot -Recurse -Include *.py |
    Select-String -Pattern '^\s*(import|from)\s+([a-zA-Z0-9_\.]+)' |
    ForEach-Object {
        $matches = $_.Matches
        foreach ($m in $matches) {
            $pkg = $m.Groups[2].Value.Split('.')[0]
            $pkg
        }
    } |
    Where-Object { $_ -and ($stdlib -notcontains $_) } |
    Sort-Object -Unique

Write-Host "Найдено внешних пакетов: $($imports.Count)" -ForegroundColor Green
$imports | ForEach-Object { Write-Host " - $_" }

# Сохраняем в requirements.txt
$imports | Set-Content -Path $outputFile -Encoding UTF8

Write-Host "requirements.txt создан: $outputFile" -ForegroundColor Green
