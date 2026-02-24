param(
  [string]$VenvPath = ".venv"
)

$ErrorActionPreference = "Stop"
& "$VenvPath\Scripts\python.exe" -m windows_agent.main --config config/settings.local.yaml
