param(
  [string]$VenvPath = ".venv"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path "$VenvPath\Scripts\python.exe")) {
  throw "Virtual environment not found. Run scripts/bootstrap.ps1 first."
}

$python = Resolve-Path "$VenvPath\Scripts\python.exe"
& $python -m windows_agent.service stop 2>$null
& $python -m windows_agent.service remove 2>$null
& $python -m windows_agent.service --startup auto install
& $python -m windows_agent.service start

Write-Host "Service installed and started."
