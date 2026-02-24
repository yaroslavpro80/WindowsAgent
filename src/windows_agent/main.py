from __future__ import annotations

import argparse
import time
from pathlib import Path

from .config import load_settings
from .runtime import AgentRuntime



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Windows Agent")
    parser.add_argument("--config", default="config/settings.local.yaml", help="Path to settings yaml")
    parser.add_argument("--action", default="", help="Optional one-shot action")
    parser.add_argument("--package-id", default="", help="Package id for install/uninstall")
    parser.add_argument("--to", default="", help="Email recipient")
    parser.add_argument("--subject", default="", help="Email subject")
    parser.add_argument("--body", default="", help="Email body")
    return parser



def main() -> int:
    args = build_parser().parse_args()
    config_path = Path(args.config)
    if not config_path.exists():
        raise FileNotFoundError(f"Missing config: {config_path}")

    settings = load_settings(config_path)
    runtime = AgentRuntime(settings)
    runtime.start()

    if args.action:
        payload = {
            "package_id": args.package_id,
            "to": args.to,
            "subject": args.subject,
            "body": args.body,
        }
        print(runtime.execute_action(args.action, payload))
        runtime.stop()
        return 0

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        runtime.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
