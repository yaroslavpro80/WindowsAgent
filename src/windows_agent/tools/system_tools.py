from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


class SystemTools:
    def __init__(self, project_root: Path | None = None) -> None:
        self.project_root = project_root or Path.cwd()

    def run_powershell(self, command: str) -> CommandResult:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            check=False,
        )
        return CommandResult(proc.returncode, proc.stdout.strip(), proc.stderr.strip())

    def run_script(self, script_relative_path: str, args: str = "") -> CommandResult:
        script = self.project_root / script_relative_path
        escaped = str(script).replace("'", "''")
        cmd = f"& '{escaped}' {args}".strip()
        return self.run_powershell(cmd)

    def install_app(self, package_id: str) -> CommandResult:
        return self.run_powershell(f"winget install --id {package_id} -e --silent")

    def uninstall_app(self, package_id: str) -> CommandResult:
        return self.run_powershell(f"winget uninstall --id {package_id} -e")

    def check_updates(self) -> CommandResult:
        return self.run_powershell("winget upgrade")

    def emergency_hide(self) -> CommandResult:
        return self.run_script("scripts/emergency_hide.ps1")

    def full_uninstall(self) -> CommandResult:
        return self.run_script("scripts/full_uninstall.ps1", "-Confirm 'ТАК' -ConfirmAgain 'ТАК'")
