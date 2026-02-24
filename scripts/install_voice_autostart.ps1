param(
  [string]$VoiceMacroExe = "C:\Program Files (x86)\VoiceMacro\VoiceMacro.exe",
  [string]$ProjectRoot = "D:\Work_Cbtl\WindowsAgent"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $VoiceMacroExe)) {
  throw "VoiceMacro executable not found: $VoiceMacroExe"
}

$startup = [Environment]::GetFolderPath("Startup")
$bridgeScript = Join-Path $ProjectRoot "scripts\clipboard_bridge.ps1"

if (-not (Test-Path $bridgeScript)) {
  throw "Bridge script not found: $bridgeScript"
}

$wsh = New-Object -ComObject WScript.Shell

$voiceShortcutPath = Join-Path $startup "VoiceMacro.lnk"
$voiceShortcut = $wsh.CreateShortcut($voiceShortcutPath)
$voiceShortcut.TargetPath = $VoiceMacroExe
$voiceShortcut.WorkingDirectory = Split-Path $VoiceMacroExe -Parent
$voiceShortcut.Save()

$bridgeShortcutPath = Join-Path $startup "WindowsAgentClipboardBridge.lnk"
$bridgeShortcut = $wsh.CreateShortcut($bridgeShortcutPath)
$bridgeShortcut.TargetPath = "$PSHOME\powershell.exe"
$bridgeShortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$bridgeScript`""
$bridgeShortcut.WorkingDirectory = $ProjectRoot
$bridgeShortcut.Save()

Start-Process -FilePath $VoiceMacroExe -WindowStyle Minimized
Start-Process -FilePath "$PSHOME\powershell.exe" -ArgumentList "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$bridgeScript`"" -WindowStyle Hidden

Write-Output "Autostart configured for VoiceMacro and clipboard bridge."
Write-Output "Inbox file: D:\Work_Cbtl\WindowsAgent\runtime\voice_inbox.txt"
