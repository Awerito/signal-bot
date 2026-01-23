from signalbot import Context

from app.cmds.base import FilteredCommand


class HelpCommand(FilteredCommand):
    async def execute(self, context: Context):
        if context.message.text == "!help":
            await context.send(
                "commands:\n"
                "!chat | !grok - responde a un mensaje para análisis\n"
                "!tldr - resumen del chat\n"
                "!grye <pregunta> - consulta libre"
            )
