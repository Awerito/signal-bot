import re

from signalbot import Context

from app.cmds.base import FilteredCommand
from app.crypto import get_prompts

# Compiled triggers cache
_triggers: list[tuple[re.Pattern, str]] | None = None


def _get_triggers() -> list[tuple[re.Pattern, str]]:
    """Load and compile triggers from encrypted prompts."""
    global _triggers
    if _triggers is None:
        prompts = get_prompts()
        _triggers = []
        for t in prompts.get("triggers", []):
            flags = getattr(re, t.get("flags", ""), 0)
            pattern = re.compile(t["pattern"], flags)
            _triggers.append((pattern, t["response"]))
    return _triggers


class TriggerCommand(FilteredCommand):
    """Auto-replies based on message patterns."""

    async def execute(self, context: Context) -> None:
        text = (context.message.text or "").strip()

        for pattern, response in _get_triggers():
            if pattern.search(text):
                await context.reply(response)
                return
