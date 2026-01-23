from signalbot import Command, Context

from app import config


class FilteredCommand(Command):
    """Base command that only responds to whitelisted groups."""

    async def handle(self, context: Context):
        group = context.message.group

        # Ignore if not a group message
        if not group:
            return

        # If whitelist is configured, check it
        if config.ALLOWED_GROUPS and group not in config.ALLOWED_GROUPS:
            return

        await self.execute(context)

    async def execute(self, context: Context):
        """Override this method in subclasses."""
        raise NotImplementedError
