from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class Decision:
    allowed: bool
    requires_confirmation: bool
    requires_pin: bool
    reason: str


class SafetyPolicy:
    def __init__(self, config: dict) -> None:
        sec = config.get("security", {})
        self.confirm_set = set(sec.get("require_confirmation_for", []))
        self.pin_set = set(sec.get("critical_require_pin_for", []))

    def evaluate(self, action: str) -> Decision:
        if action in self.pin_set:
            return Decision(True, True, True, "critical action")
        if action in self.confirm_set:
            return Decision(True, True, False, "sensitive action")
        return Decision(True, False, False, "safe action")

    @staticmethod
    def format_actions(actions: Iterable[str]) -> str:
        return ", ".join(actions)
