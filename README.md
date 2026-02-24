# WindowsAgent

Personal assistant scaffold for Windows 11 with service mode, safety policy, voice wake-word loop, and Microsoft Graph mail/calendar integration.

## What is included
- Agent runtime with scheduler and audit logging
- Action execution (`check_updates`, `install_app`, `uninstall_app`, `send_email`, `morning_brief`)
- Safety policy (safe/sensitive/critical)
- Voice pipeline (STT/TTS with fallback if audio dependencies are unavailable)
- Microsoft Graph integration (`list_priority_mail`, `today_events`, `send_email`)
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
.\.venv\Scripts\python.exe -m windows_agent.main --config config/settings.local.yaml --action morning_brief
```

## Voice loop
```powershell
.\.venv\Scripts\python.exe -m windows_agent.main --config config/settings.local.yaml --voice-loop
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

## Microsoft Graph setup
1. Register app in Entra ID.
2. Grant application permissions: `Mail.Read`, `Mail.Send`, `Calendars.Read`.
3. Fill `integrations.microsoft_graph` in `config/settings.local.yaml`.
4. If you use delegated mailbox, set `user_principal_name`.

## Next implementation tasks
- Add tray GUI for approvals and live status.
- Add explicit command allowlist and human confirmation flow for sensitive actions.
- Add plugin-based task packs (backup, browser, notes, reminders).
