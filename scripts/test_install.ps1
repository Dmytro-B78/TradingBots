# ================================================================
# NT-Tech Installer Test
# ASCII-only, no Cyrillic
# Purpose:
#   Validate that PowerShell correctly interprets NT-Tech Mode blocks.
#   This script does NOT create files or directories.
#   It only prints the resolved base path.
# ================================================================

Write-Host "NT-Tech Installer Test Started..."

$base = "C:\TradingBots\NT"

Write-Host "Resolved base path:"
Write-Host $base

Write-Host "Test completed."
