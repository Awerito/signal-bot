"""Decrypt encrypted prompts at runtime."""

import json
from pathlib import Path

from cryptography.fernet import Fernet

from app import config

_fernet: Fernet | None = None
_prompts: dict | None = None

PROMPTS_FILE = Path(__file__).parent / "prompts.enc.json"


def _get_fernet() -> Fernet:
    global _fernet
    if _fernet is None:
        _fernet = Fernet(config.PROMPT_KEY.encode())
    return _fernet


def _decrypt(value):
    """Recursively decrypt string values in a data structure."""
    fernet = _get_fernet()
    if isinstance(value, str):
        return fernet.decrypt(value.encode()).decode()
    elif isinstance(value, dict):
        return {k: _decrypt(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_decrypt(item) for item in value]
    return value


def get_prompts() -> dict:
    """Load and decrypt prompts. Cached after first call."""
    global _prompts
    if _prompts is None:
        with open(PROMPTS_FILE) as f:
            encrypted = json.load(f)
        _prompts = _decrypt(encrypted)
    return _prompts
