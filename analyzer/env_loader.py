"""Shared .env loader.

Reads the project's .env file (if present) and sets the resulting key/value
pairs in os.environ. Override behavior is intentional:

  - If a key is missing from the environment, set from .env.
  - If a key is present in the environment but EMPTY, set from .env. This
    handles the Windows gotcha where `$env:FOO = ""` leaves the variable
    present-but-empty.
  - If a key is present with a real value, leave it alone — explicit
    shell exports win over .env.

Both web/app.py and analyzer/__main__.py call this so the CLI and the web UI
behave the same way.
"""
from __future__ import annotations

import os
from pathlib import Path


def load_env(env_path: str | Path | None = None) -> dict[str, str]:
    """Load .env into os.environ. Returns the dict of values that were set
    by THIS call (useful for diagnostics; never logs the actual values)."""
    if env_path is None:
        # Default: project root (the directory containing the analyzer/ package).
        env_path = Path(__file__).resolve().parent.parent / ".env"
    env_path = Path(env_path)
    if not env_path.is_file():
        return {}

    set_keys: dict[str, str] = {}
    # utf-8-sig tolerates a UTF-8 BOM that Notepad sometimes prepends.
    for line in env_path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if not os.environ.get(k):  # missing OR empty -> set from .env
            os.environ[k] = v
            set_keys[k] = "set"
    return set_keys
