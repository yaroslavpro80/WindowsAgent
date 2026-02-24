$ErrorActionPreference = "Continue"

$startup = [Environment]::GetFolderPath("Startup")
$voiceShortcutPath = Join-Path $startup "VoiceMacro.lnk"
$bridgeShortcutPath = Join-Path $startup "WindowsAgentClipboardBridge.lnk"

if (Test-Path $voiceShortcutPath) {
  Remove-Item $voiceShortcutPath -Force
}
if (Test-Path $bridgeShortcutPath) {
  Remove-Item $bridgeShortcutPath -Force
}

Get-Process -Name VoiceMacro -ErrorAction SilentlyContinue | Stop-Process -Force

$bridgeProc = Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" -ErrorAction SilentlyContinue |
  Where-Object { $_.CommandLine -match 'clipboard_bridge.ps1' }
foreach ($p in $bridgeProc) {
  Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
}

Write-Output "Voice autostart disabled and related processes stopped."
