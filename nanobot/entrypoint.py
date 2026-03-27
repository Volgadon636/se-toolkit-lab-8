#!/usr/bin/env python3
"""Resolve Docker env vars into nanobot config, then exec nanobot gateway."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

VENV_PYTHON = os.environ.get("NANOBOT_VENV_PYTHON", "/app/nanobot/.venv/bin/python")
NANOBOT_BIN = os.environ.get("NANOBOT_CLI", "/app/nanobot/.venv/bin/nanobot")


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
    resolved_path = root / "config.resolved.json"
    workspace = os.environ.get("NANOBOT_WORKSPACE", str(root / "workspace"))

    access_key = os.environ.get("NANOBOT_ACCESS_KEY", "").strip()
    if not access_key:
        print(
            "FATAL: NANOBOT_ACCESS_KEY is empty or missing. Set it in .env.docker.secret.",
            file=sys.stderr,
        )
        sys.exit(1)

    llm_key = os.environ.get("LLM_API_KEY", "").strip()
    if not llm_key:
        print(
            "FATAL: LLM_API_KEY is empty (maps from Qwen / LLM in compose).",
            file=sys.stderr,
        )
        sys.exit(1)

    data = json.loads(cfg_path.read_text(encoding="utf-8"))

    llm_base = os.environ.get("LLM_API_BASE_URL", "").strip().rstrip("/")
    llm_model = os.environ.get("LLM_API_MODEL", "coder-model").strip()

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
                    "workspace": workspace,
                }
            },
            "gateway": {
                "host": os.environ.get(
                    "NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0"
                ),
                "port": int(
                    os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "18790")
                ),
            },
            "channels": {
                "webchat": {
                    "enabled": True,
                    "host": os.environ.get(
                        "NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0"
                    ),
                    "port": int(
                        os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765")
                    ),
                    "allow_from": ["*"],
                }
            },
            "tools": {
                "mcpServers": {
                    "lms": {
                        "command": VENV_PYTHON,
                        "args": ["-m", "mcp_lms"],
                        "env": {
                            "NANOBOT_LMS_BACKEND_URL": os.environ.get(
                                "NANOBOT_LMS_BACKEND_URL", ""
                            ),
                            "NANOBOT_LMS_API_KEY": os.environ.get(
                                "NANOBOT_LMS_API_KEY", ""
                            ),
                            "VICTORIALOGS_BASE_URL": os.environ.get(
                                "VICTORIALOGS_BASE_URL", ""
                            ),
                            "VICTORIATRACES_BASE_URL": os.environ.get(
                                "VICTORIATRACES_BASE_URL", ""
                            ),
                        },
                    }
                }
            },
        },
    )

    resolved_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # Fail fast if config is invalid (same validation nanobot uses).
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

    os.execve(
        NANOBOT_BIN,
        [
            NANOBOT_BIN,
            "gateway",
            "--config",
            str(resolved_path),
            "--workspace",
            workspace,
        ],
        os.environ,
    )


if __name__ == "__main__":
    main()
