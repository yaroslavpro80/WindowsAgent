from __future__ import annotations

from dataclasses import dataclass

from apscheduler.schedulers.background import BackgroundScheduler

from .config import Settings
from .integrations.mail_calendar import MailCalendarClient
from .safety.policy import SafetyPolicy
from .storage.audit import AuditLog
from .tools.system_tools import SystemTools
from .voice.pipeline import VoicePipeline


@dataclass
class AgentRuntime:
    settings: Settings

    def __post_init__(self) -> None:
        self.audit = AuditLog(self.settings.audit_log_path)
        self.policy = SafetyPolicy(self.settings.raw)
        self.tools = SystemTools()
        enabled = bool(self.settings.raw.get("integrations", {}).get("microsoft_graph", {}).get("enabled", False))
        self.mail = MailCalendarClient(enabled=enabled)
        wake_word = self.settings.raw.get("agent", {}).get("wake_word", "assistant")
        self.voice = VoicePipeline(wake_word=wake_word)
        self.scheduler = BackgroundScheduler(timezone=self.settings.timezone)

    def start(self) -> None:
        self.audit.write("agent_start", f"name={self.settings.agent_name}")
        self.scheduler.start()
        self.scheduler.add_job(self.daily_digest, "cron", hour=8, minute=30, id="daily_digest", replace_existing=True)

    def stop(self) -> None:
        self.scheduler.shutdown(wait=False)
        self.audit.write("agent_stop", "manual_or_service_stop")

    def daily_digest(self) -> None:
        events = self.mail.today_events()
        summary = f"events={len(events)}"
        self.audit.write("daily_digest", summary)

    def execute_action(self, action: str, payload: dict[str, str]) -> str:
        decision = self.policy.evaluate(action)
        self.audit.write("policy_check", f"action={action};reason={decision.reason}")

        if action == "check_updates":
            result = self.tools.check_updates()
            self.audit.write("check_updates", f"rc={result.returncode}")
            return result.stdout or result.stderr

        if action == "install_app":
            pkg = payload.get("package_id", "")
            result = self.tools.install_app(pkg)
            self.audit.write("install_app", f"pkg={pkg};rc={result.returncode}")
            return result.stdout or result.stderr

        if action == "uninstall_app":
            pkg = payload.get("package_id", "")
            result = self.tools.uninstall_app(pkg)
            self.audit.write("uninstall_app", f"pkg={pkg};rc={result.returncode}")
            return result.stdout or result.stderr

        if action == "send_email":
            ok = self.mail.send_email(
                to=payload.get("to", ""),
                subject=payload.get("subject", ""),
                body=payload.get("body", ""),
            )
            self.audit.write("send_email", f"ok={ok}")
            return "sent" if ok else "integration_disabled"

        return f"unknown action: {action}"
