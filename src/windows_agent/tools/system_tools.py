from __future__ import annotations

import subprocess
from dataclasses import dataclass


@dataclass
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


class SystemTools:
    def run_powershell(self, command: str) -> CommandResult:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            check=False,
        )
        return CommandResult(proc.returncode, proc.stdout.strip(), proc.stderr.strip())

    def install_app(self, package_id: str) -> CommandResult:
        return self.run_powershell(f"winget install --id {package_id} -e --silent")

    def uninstall_app(self, package_id: str) -> CommandResult:
        return self.run_powershell(f"winget uninstall --id {package_id} -e")

    def check_updates(self) -> CommandResult:
        return self.run_powershell("winget upgrade")
