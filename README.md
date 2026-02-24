# WindowsAgent

Personal assistant scaffold for Windows 11 with service mode, safety policy, automation hooks, voice pipeline placeholder, and mail/calendar integration stubs.

## What is included
- Agent runtime with scheduler and audit logging
- Action execution (`check_updates`, `install_app`, `uninstall_app`, `send_email`)
- Safety policy (safe/sensitive/critical)
- Windows Service entrypoint (pywin32)
- Bootstrap, run, service install/uninstall scripts
- Config template and minimal unit test

## Quick start
1. Open PowerShell in project root.
2. Run:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1
```
3. Edit `config/settings.local.yaml` and set integration secrets.
4. Run in dev mode:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_dev.ps1
```

## One-shot actions
```powershell
.\.venv\Scripts\python.exe -m windows_agent.main --config config/settings.local.yaml --action check_updates
.\.venv\Scripts\python.exe -m windows_agent.main --config config/settings.local.yaml --action install_app --package-id Telegram.TelegramDesktop
```

## Install as Windows service
Run PowerShell as Administrator:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_service.ps1
```

Uninstall:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/uninstall_service.ps1
```

## GitHub
```powershell
git add .
git commit -m "Initial WindowsAgent scaffold"
git remote add origin <your-github-repo-url>
git push -u origin main
```

## Next implementation tasks
- Replace `voice/pipeline.py` with real STT/TTS and wake word.
- Implement OAuth + Microsoft Graph in `integrations/mail_calendar.py`.
- Add GUI tray app for confirmations and live status.
- Add allowlist policy for PowerShell commands and tools.
