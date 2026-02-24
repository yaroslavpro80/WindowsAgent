from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MailItem:
    sender: str
    subject: str


class MailCalendarClient:
    """Stub for Microsoft Graph integration."""

    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled

    def list_priority_mail(self) -> list[MailItem]:
        if not self.enabled:
            return []
        return []

    def send_email(self, to: str, subject: str, body: str) -> bool:
        if not self.enabled:
            return False
        return True

    def today_events(self) -> list[str]:
        if not self.enabled:
            return []
        return []
