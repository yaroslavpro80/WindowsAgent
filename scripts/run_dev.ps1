param(
  [string]$VenvPath = ".venv"
)

$ErrorActionPreference = "Stop"
if (-not (Test-Path "$VenvPath\Scripts\python.exe")) {
  throw "Virtual environment not found. Run scripts/bootstrap.ps1 first."
}
& "$VenvPath\Scripts\python.exe" -m windows_agent.main --config config/settings.local.yaml
