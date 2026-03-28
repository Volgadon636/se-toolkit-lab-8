#!/usr/bin/env python3
"""Resolve Docker env vars into nanobot config, then exec nanobot gateway."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

VENV_PYTHON = os.environ.get("NANOBOT_VENV_PYTHON", "/app/nanobot/.venv/bin/python")
WORKSPACE_DIR = os.environ.get("NANOBOT_WORKSPACE", "/app/nanobot/workspace")


def _deep_merge(base: dict, updates: dict) -> None:
    for key, val in updates.items():
        if (
            key in base
            and isinstance(base[key], dict)
            and isinstance(val, dict)
        ):
            _deep_merge(base[key], val)
        else:
            base[key] = val


def main() -> None:
    root = Path(__file__).resolve().parent
    cfg_path = root / "config.json"
    resolved_path = Path("/app/nanobot/config.resolved.json")

    access_key = os.environ.get("NANOBOT_ACCESS_KEY", "").strip()
    if not access_key:
        print(
            "FATAL: NANOBOT_ACCESS_KEY is empty or missing.",
            file=sys.stderr,
        )
        sys.exit(1)

    llm_key = os.environ.get("LLM_API_KEY", "").strip()
    if not llm_key:
        print("FATAL: LLM_API_KEY is empty.", file=sys.stderr)
        sys.exit(1)

    # Prefer LLM_API_BASE (as in .env.docker.secret); fallback to LLM_API_BASE_URL from compose.
    llm_base = os.environ.get("LLM_API_BASE", "").strip().rstrip("/")
    if not llm_base:
        llm_base = os.environ.get("LLM_API_BASE_URL", "").strip().rstrip("/")
    if not llm_base:
        print(
            "FATAL: Set LLM_API_BASE or LLM_API_BASE_URL to the Qwen OpenAI base URL.",
            file=sys.stderr,
        )
        sys.exit(1)

    llm_model = os.environ.get("LLM_API_MODEL", "coder-model").strip()

    def _strip_env(key: str, default: str = "") -> str:
        return os.environ.get(key, default).strip()

    data = json.loads(cfg_path.read_text(encoding="utf-8"))

    gateway_port = int(
        os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "18790")
    )
    webchat_port = int(
        os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765")
    )

    _deep_merge(
        data,
        {
            "providers": {
                "custom": {
                    "apiKey": llm_key,
                    "apiBase": llm_base,
                }
            },
            "agents": {
                "defaults": {
                    "model": llm_model,
                    "provider": "custom",
                    "workspace": WORKSPACE_DIR,
                }
            },
            "gateway": {
                "host": os.environ.get(
                    "NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0"
                ),
                "port": gateway_port,
            },
            "channels": {
                "webchat": {
                    "enabled": True,
                    "host": os.environ.get(
                        "NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0"
                    ),
                    "port": webchat_port,
                    "allow_from": ["*"],
                }
            },
            "tools": {
                "mcpServers": {
                    "lms": {
                        "command": VENV_PYTHON,
                        "args": ["-m", "mcp_lms"],
                        "env": {
                            "NANOBOT_LMS_BACKEND_URL": _strip_env(
                                "NANOBOT_LMS_BACKEND_URL", ""
                            ),
                            "NANOBOT_LMS_API_KEY": _strip_env(
                                "NANOBOT_LMS_API_KEY", ""
                            ),
                            "VICTORIALOGS_BASE_URL": _strip_env(
                                "VICTORIALOGS_BASE_URL", ""
                            ),
                            "VICTORIATRACES_BASE_URL": _strip_env(
                                "VICTORIATRACES_BASE_URL", ""
                            ),
                        },
                    }
                }
            },
        },
    )

    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    cfg_check = (
        "import json\n"
        "from pathlib import Path\n"
        "from nanobot.config.schema import Config\n"
        f"p = Path({str(resolved_path)!r})\n"
        "Config.model_validate(json.loads(p.read_text(encoding='utf-8')))\n"
    )
    try:
        subprocess.run(
            [VENV_PYTHON, "-c", cfg_check],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        print("FATAL: nanobot config validation failed:", file=sys.stderr)
        print(exc.stderr or exc.stdout, file=sys.stderr)
        sys.exit(1)

    # NANOBOT_ACCESS_KEY is read by the webchat channel from the environment (not config JSON).
    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--config",
            str(resolved_path),
            "--workspace",
            WORKSPACE_DIR,
        ],
    )


if __name__ == "__main__":
    main()
