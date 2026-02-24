from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


class AuditLog:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, event: str, details: str) -> None:
        ts = datetime.now(timezone.utc).isoformat()
        line = f"{ts} | {event} | {details}\n"
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line)
