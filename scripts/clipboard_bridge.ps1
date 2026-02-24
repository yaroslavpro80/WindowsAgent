param(
  [string]$InboxPath = "D:\Work_Cbtl\WindowsAgent\runtime\voice_inbox.txt",
  [string]$LogPath = "D:\Work_Cbtl\WindowsAgent\runtime\voice_inbox.log",
  [int]$PollMs = 600
)

$ErrorActionPreference = "Continue"
Add-Type -AssemblyName System.Windows.Forms

$inboxDir = Split-Path $InboxPath -Parent
New-Item -ItemType Directory -Force -Path $inboxDir | Out-Null

$last = ""

while ($true) {
  try {
    $text = [Windows.Forms.Clipboard]::GetText()
    if ($text -and $text -ne $last) {
      $last = $text
      $ts = Get-Date -Format o
      $payload = "[$ts] $text"
      Set-Content -Path $InboxPath -Value $payload -Encoding UTF8
      Add-Content -Path $LogPath -Value $payload -Encoding UTF8
    }
  } catch {
    # Ignore clipboard lock/contention errors and keep listening.
  }
  Start-Sleep -Milliseconds $PollMs
}
