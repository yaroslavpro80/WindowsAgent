param(
  [string]$VenvPath = ".venv"
)

$ErrorActionPreference = "Stop"

function Resolve-Python {
  $candidates = @()
  $cmdPython = Get-Command python -ErrorAction SilentlyContinue
  if ($cmdPython -and $cmdPython.Source) {
    $candidates += $cmdPython.Source
  }
  $candidates += @(
    "C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python312\\python.exe",
    "C:\\Program Files\\Python312\\python.exe"
  )

  foreach ($candidate in $candidates) {
    if (-not $candidate -or -not (Test-Path $candidate)) { continue }
    try {
      & $candidate --version | Out-Null
      if ($LASTEXITCODE -eq 0) { return $candidate }
    } catch {
      continue
    }
  }
  throw "Python not found. Install Python and rerun bootstrap."
}

if (-not (Test-Path "config/settings.local.yaml")) {
  Copy-Item "config/settings.example.yaml" "config/settings.local.yaml"
}

$pythonExe = Resolve-Python
& $pythonExe -m venv $VenvPath
& "$VenvPath\Scripts\python.exe" -m pip install --upgrade pip
& "$VenvPath\Scripts\python.exe" -m pip install -r requirements.txt
& "$VenvPath\Scripts\python.exe" -m pip install -e .

Write-Host "Bootstrap complete. Edit config/settings.local.yaml before enabling integrations."
