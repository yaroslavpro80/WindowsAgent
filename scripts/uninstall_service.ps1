$ErrorActionPreference = "Continue"
sc.exe stop WindowsAgentService | Out-Host
sc.exe delete WindowsAgentService | Out-Host
Write-Host "Service removed."
