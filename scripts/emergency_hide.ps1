$ErrorActionPreference = "Continue"

$projectRoot = Split-Path $PSScriptRoot -Parent
$runtimeDir = Join-Path $projectRoot "runtime"
$flagPath = Join-Path $runtimeDir "disabled.flag"

New-Item -ItemType Directory -Force -Path $runtimeDir | Out-Null
Set-Content -Path $flagPath -Value ("disabled_at=" + (Get-Date -Format o)) -Encoding UTF8

sc.exe stop WindowsAgentService | Out-Null
sc.exe config WindowsAgentService start= demand | Out-Null

Write-Output "Agent disabled. Service stopped and autostart disabled."
