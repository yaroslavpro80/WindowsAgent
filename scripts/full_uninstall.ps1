param(
  [string]$Confirm = "",
  [string]$ConfirmAgain = ""
)

$ErrorActionPreference = "Continue"

if ($Confirm -ne "ТАК" -or $ConfirmAgain -ne "ТАК") {
  Write-Output "Uninstall aborted: double confirmation not provided."
  exit 1
}

$projectRoot = Split-Path $PSScriptRoot -Parent

& (Join-Path $PSScriptRoot "emergency_hide.ps1") | Out-Null
& (Join-Path $PSScriptRoot "uninstall_service.ps1") | Out-Null

$targets = @(
  (Join-Path $projectRoot ".venv"),
  (Join-Path $projectRoot "logs"),
  (Join-Path $projectRoot "runtime"),
  (Join-Path $projectRoot "config\\settings.local.yaml")
)

foreach ($target in $targets) {
  if (Test-Path $target) {
    try {
      Remove-Item -Path $target -Recurse -Force
    } catch {
      Write-Output ("Could not remove: " + $target)
    }
  }
}

Write-Output "WindowsAgent components removed (service, venv, runtime, logs, local config)."
