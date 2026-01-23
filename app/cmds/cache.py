from signalbot import Command, Context

from app import config
from app import redis_client


class MessageCacheCommand(Command):
    """Silently caches all messages from allowed groups."""

    async def handle(self, context: Context) -> None:
        group = context.message.group
        text = context.message.text

        # Only cache group messages with text
        if not group or not text:
            return

        # Respect group whitelist
        if config.ALLOWED_GROUPS and group not in config.ALLOWED_GROUPS:
            return

        await redis_client.cache_message(
            group_id=group,
            timestamp=context.message.timestamp,
            text=text,
            author=context.message.source,
        )
