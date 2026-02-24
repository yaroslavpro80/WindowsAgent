# PROJECT STATUS (2026-02-24)

## Current state
- Repository: `https://github.com/yaroslavpro80/WindowsAgent.git`
- Branch: `main`
- Implemented:
  - Agent runtime with scheduler and audit log.
  - Core actions: `check_updates`, `install_app`, `uninstall_app`, `send_email`, `morning_brief`.
  - Voice loop with wake word and Ukrainian STT/TTS defaults.
  - Emergency self-disable flow (`emergency_hide`) with user confirmation.
  - Full uninstall flow (`full_uninstall`) with double confirmation.
  - Microsoft Graph integration layer (mail read/send, calendar read) using app credentials.
  - Windows service scripts for install/start/stop/remove.

## What is still missing
1. Production voice stack:
- Replace Google STT fallback with stable provider (Azure Speech or local Whisper).
- Add deterministic wake-word engine (Porcupine/openWakeWord) instead of phrase matching only.

2. Safer action execution:
- Enforce command allowlist in `SystemTools`.
- Add mandatory approval UI for sensitive/critical actions (not voice-only).
- Add PIN/secret verification path for critical actions.

3. UI/visibility control:
- Add tray app with status, pending approvals, and panic button.
- Show current mode: active/paused/disabled.

4. Graph hardening:
- Validate permissions and token acquisition errors with clear diagnostics.
- Add mailbox/event filtering options and retry/backoff.

5. Installer hardening:
- Add single setup script for first-time provisioning (runtime + service + config checks).
- Add optional packaged distribution (MSI/EXE or self-contained installer).

## Open technical risks
- `pyttsx3` and microphone stack can behave differently across Windows builds/audio drivers.
- Service mode + audio capture may fail depending on session isolation and service account.
- `full_uninstall.ps1` currently removes service/venv/runtime/logs/local config, but intentionally keeps source repo.

## Recommended next implementation order
1. Build tray approval app (minimal UI).
2. Add allowlist + policy enforcement in execution layer.
3. Replace STT/wake-word implementation with deterministic engine.
4. Harden Graph auth diagnostics and add integration tests.
5. Add one-command installer and service health watchdog.

## Next-session prompt
`Продовжити проект WindowsAgent. Виконай пункти з docs/PROJECT_STATUS.md у рекомендованому порядку, починаючи з tray approval app + allowlist.`
