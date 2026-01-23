import os

from dotenv import load_dotenv

load_dotenv()

PHONE_NUMBER = os.getenv("PHONE_NUMBER")
SIGNAL_SERVICE = os.getenv("SIGNAL_SERVICE", "localhost:8080")


def _parse_list(value: str | None) -> list[str]:
    """Parse comma-separated env var into list, stripping whitespace."""
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


# Whitelist: only respond to these groups. Empty = allow all.
ALLOWED_GROUPS = _parse_list(os.getenv("ALLOWED_GROUPS"))

# Redis config
REDIS_URI = os.getenv("REDIS_URI", "redis://localhost:6379")
REDIS_DB = 2
MESSAGE_CACHE_TTL = 2 * 60 * 60  # 2 hours in seconds

# Groq config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"

# Encryption key for prompts
PROMPT_KEY = os.getenv("PROMPT_KEY")
