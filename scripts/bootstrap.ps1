param(
  [string]$VenvPath = ".venv"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path "config/settings.local.yaml")) {
  Copy-Item "config/settings.example.yaml" "config/settings.local.yaml"
}

python -m venv $VenvPath
& "$VenvPath\Scripts\python.exe" -m pip install --upgrade pip
& "$VenvPath\Scripts\python.exe" -m pip install -r requirements.txt

Write-Host "Bootstrap complete. Edit config/settings.local.yaml before enabling integrations."
