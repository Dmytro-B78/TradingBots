# ============================================
# File: update_whitelist.ps1
# Purpose: Convert whitelist.csv to whitelist.json
# Logging: UTF-8 without BOM, ASCII-only messages
# ============================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# File paths
$csvPath = "C:\TradingBots\NT\data\whitelist.csv"
$jsonPath = "C:\TradingBots\NT\data\whitelist.json"
$logPath = "C:\TradingBots\NT\logs\whitelist.log"

# Ensure log directory exists
$logDir = Split-Path $logPath
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

# Logging function (pure UTF-8 without BOM)
function Log-Message {
    param([string]$message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $fullMessage = "$timestamp $message"
    $writer = [System.IO.StreamWriter]::new($logPath, $true, [System.Text.Encoding]::UTF8)
    $writer.WriteLine($fullMessage)
    $writer.Close()
    Write-Host $message
}

# Main logic
if (Test-Path $csvPath) {
    try {
        $csv = Import-Csv -Path $csvPath
        $json = $csv | ConvertTo-Json -Depth 3
        Set-Content -Path $jsonPath -Value $json -Encoding UTF8
        Log-Message "whitelist.json updated from whitelist.csv"
    }
    catch {
        Log-Message "ERROR: Failed to update whitelist.json"
        Log-Message $_.Exception.Message
    }
}
else {
    Log-Message "ERROR: whitelist.csv not found at $csvPath"
}
