param(
  [string]$VenvPath = ".venv"
)

$ErrorActionPreference = "Stop"

$python = Resolve-Path "$VenvPath\Scripts\python.exe"
$binPath = '"' + $python + '" -m windows_agent.service --startup auto install'

sc.exe create WindowsAgentService binPath= $binPath start= auto | Out-Host
sc.exe description WindowsAgentService "Windows Personal Agent Service" | Out-Host
sc.exe start WindowsAgentService | Out-Host

Write-Host "Service installed and started."
