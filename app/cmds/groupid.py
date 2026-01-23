import asyncio

from signalbot import Context

from app.cmds.base import FilteredCommand


class GroupIdCommand(FilteredCommand):
    async def execute(self, context: Context):
        if context.message.text == "!groupid":
            ts = await context.send(f"group id: {context.message.group}")
            await asyncio.sleep(60)
            await context.remote_delete(ts)
