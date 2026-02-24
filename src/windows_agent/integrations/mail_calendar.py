from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import requests

try:
    import msal
except Exception:  # pragma: no cover - optional runtime dependency in some environments
    msal = None


@dataclass
class MailItem:
    sender: str
    subject: str


class MailCalendarClient:
    GRAPH_BASE = "https://graph.microsoft.com/v1.0"

    def __init__(self, enabled: bool, graph_config: dict[str, Any] | None = None) -> None:
        self.enabled = enabled
        cfg = graph_config or {}
        self.tenant_id = cfg.get("tenant_id", "")
        self.client_id = cfg.get("client_id", "")
        self.client_secret = cfg.get("client_secret", "")
        self.user_principal_name = cfg.get("user_principal_name", "")
        self.scopes = cfg.get(
            "scopes",
            ["User.Read", "Mail.Read", "Mail.Send", "Calendars.Read"],
        )
        self._token: str | None = None

    def _is_ready(self) -> bool:
        return (
            self.enabled
            and msal is not None
            and bool(self.tenant_id and self.client_id and self.client_secret)
        )

    def _acquire_token(self) -> str | None:
        if not self._is_ready():
            return None
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            authority=authority,
            client_credential=self.client_secret,
        )
        scope_values = self.scopes
        if not any(s.endswith(".default") for s in scope_values):
            scope_values = ["https://graph.microsoft.com/.default"]
        result = app.acquire_token_for_client(scopes=scope_values)
        token = result.get("access_token")
        self._token = token
        return token

    def _headers(self) -> dict[str, str]:
        token = self._token or self._acquire_token()
        if not token:
            return {}
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def list_priority_mail(self) -> list[MailItem]:
        headers = self._headers()
        if not headers:
            return []
        user_segment = f"/users/{self.user_principal_name}" if self.user_principal_name else "/me"
        url = (
            f"{self.GRAPH_BASE}{user_segment}/messages"
            "?$top=10&$select=subject,from,importance,isRead,receivedDateTime"
            "&$orderby=receivedDateTime desc"
        )
        try:
            r = requests.get(url, headers=headers, timeout=20)
        except requests.RequestException:
            return []
        if r.status_code >= 400:
            return []
        data = r.json().get("value", [])
        items: list[MailItem] = []
        for m in data:
            if m.get("importance") == "high" or not m.get("isRead", True):
                sender = (
                    m.get("from", {})
                    .get("emailAddress", {})
                    .get("address", "unknown")
                )
                items.append(MailItem(sender=sender, subject=m.get("subject", "")))
        return items

    def send_email(self, to: str, subject: str, body: str) -> bool:
        headers = self._headers()
        if not headers:
            return False
        user_segment = f"/users/{self.user_principal_name}" if self.user_principal_name else "/me"
        url = f"{self.GRAPH_BASE}{user_segment}/sendMail"
        payload = {
            "message": {
                "subject": subject,
                "body": {"contentType": "Text", "content": body},
                "toRecipients": [{"emailAddress": {"address": to}}],
            },
            "saveToSentItems": True,
        }
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=20)
        except requests.RequestException:
            return False
        if r.status_code in (200, 202):
            return True
        return False

    def today_events(self) -> list[str]:
        headers = self._headers()
        if not headers:
            return []
        start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        user_segment = f"/users/{self.user_principal_name}" if self.user_principal_name else "/me"
        url = (
            f"{self.GRAPH_BASE}{user_segment}/calendarView"
            f"?startDateTime={start.isoformat()}&endDateTime={end.isoformat()}"
            "&$select=subject,start,end&$orderby=start/dateTime"
        )
        try:
            r = requests.get(url, headers=headers, timeout=20)
        except requests.RequestException:
            return []
        if r.status_code >= 400:
            return []
        events = []
        for e in r.json().get("value", []):
            s = e.get("start", {}).get("dateTime", "")
            events.append(f"{s} {e.get('subject', 'no subject')}")
        return events
