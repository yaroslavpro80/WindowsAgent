# WINDOWS INSTALL CHECKLIST (2026-02-24)

## Already installed on this machine
- Git (`git version 2.47.0.windows.2`)
- Python 3.12 (installed via `winget`)
- GitHub CLI (`gh`) installed via `winget` (may require shell restart to appear in PATH)

## Required for development/runtime
1. Open PowerShell as Administrator.
2. In repo root run:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1
```
3. Ensure local config exists and is filled:
- `config/settings.local.yaml`
- Set Graph keys: `tenant_id`, `client_id`, `client_secret`, optional `user_principal_name`.
4. For service mode:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_service.ps1
```

## Optional but recommended
- Disable broken Store alias if `python` points to WindowsApps stub:
  - `Settings -> Apps -> Advanced app settings -> App execution aliases`
  - Turn off `python.exe` and `python3.exe` aliases there.
- Install real wake-word/STT provider (future task): Azure Speech SDK or local Whisper stack.

## Validation commands
```powershell
.\.venv\Scripts\python.exe -m compileall src
.\.venv\Scripts\python.exe -m windows_agent.main --config config/settings.local.yaml --action morning_brief
.\.venv\Scripts\python.exe -m windows_agent.main --config config/settings.local.yaml --voice-loop
```

## Emergency/Removal commands
```powershell
powershell -ExecutionPolicy Bypass -File scripts/emergency_hide.ps1
powershell -ExecutionPolicy Bypass -File scripts/full_uninstall.ps1 -Confirm "ТАК" -ConfirmAgain "ТАК"
```
