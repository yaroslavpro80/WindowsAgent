from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Settings:
    raw: dict[str, Any]

    @property
    def agent_name(self) -> str:
        return self.raw.get("agent", {}).get("name", "WindowsAgent")

    @property
    def timezone(self) -> str:
        return self.raw.get("runtime", {}).get("timezone", "Europe/Kyiv")

    @property
    def audit_log_path(self) -> Path:
        return Path(self.raw.get("runtime", {}).get("audit_log_path", "logs/audit.log"))

    @property
    def graph_config(self) -> dict[str, Any]:
        return self.raw.get("integrations", {}).get("microsoft_graph", {})

    @property
    def voice_config(self) -> dict[str, Any]:
        return self.raw.get("integrations", {}).get("voice", {})



def load_settings(path: Path) -> Settings:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return Settings(raw=data)
