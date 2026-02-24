from __future__ import annotations

import servicemanager
import win32event
import win32service
import win32serviceutil
from pathlib import Path

from .config import load_settings
from .runtime import AgentRuntime


class WindowsAgentService(win32serviceutil.ServiceFramework):
    _svc_name_ = "WindowsAgentService"
    _svc_display_name_ = "Windows Personal Agent"
    _svc_description_ = "Personal assistant agent with automation and voice pipeline"

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.runtime = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.runtime is not None:
            self.runtime.stop()
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        settings = load_settings(Path("config/settings.local.yaml"))
        self.runtime = AgentRuntime(settings)
        self.runtime.start()
        servicemanager.LogInfoMsg("WindowsAgentService started")
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(WindowsAgentService)
