import base64
import random
from pathlib import Path

from groq import AsyncGroq, RateLimitError
from signalbot import Context

from app import config
from app import redis_client
from app.cmds.base import FilteredCommand
from app.crypto import get_prompts

# Rate limit memes: (filename, message)
RATE_LIMIT_MEMES = [
    ("no.quiero.jpg", "no quiero 🤖"),
    ("sin.dinero.jpg", "Sin tokens, y no tengo pa pagar más 💸"),
    ("no.puedo.estoy.casado.jpg", "No puedo, estoy casado 😒"),
    ("homero.arbusto.jpg", "🫥"),
]

ASSETS_PATH = Path(__file__).parent.parent / "assets"


def load_image_b64(filename: str) -> str:
    """Load an image as base64 from assets folder."""
    with open(ASSETS_PATH / filename, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


class ChatCommand(FilteredCommand):
    """Fact-check command triggered by !chat as a reply."""

    def __init__(self):
        self._groq: AsyncGroq | None = None

    @property
    def groq(self) -> AsyncGroq:
        if self._groq is None:
            self._groq = AsyncGroq(api_key=config.GROQ_API_KEY)
        return self._groq

    async def _send_rate_limited(self, context: Context) -> None:
        """Send a random funny meme response when rate limited."""
        filename, message = random.choice(RATE_LIMIT_MEMES)
        image_b64 = load_image_b64(filename)
        await context.reply(message, base64_attachments=[image_b64])

    async def execute(self, context: Context) -> None:
        text = context.message.text or ""

        # Check which mode
        if text.startswith("!tldr"):
            mode = "tldr"
        elif text.startswith("!grok"):
            mode = "grok"
        elif text.startswith("!grye"):
            mode = "grye"
        elif text.startswith("!chat"):
            mode = "chat"
        else:
            return

        # !grye is a direct query
        if mode == "grye":
            query = text[5:].strip()  # Remove "!grye" prefix
            if not query:
                await context.send("usa: !grye <pregunta>")
                return
            if len(query.split()) > 20:
                await context.send("máximo 20 palabras")
                return
            # If replying to someone, include quote as context
            if context.message.quote:
                conversation = f"{context.message.quote.text}\n\n{query}"
            else:
                conversation = query
        else:
            # Must be a reply to another message
            if not context.message.quote:
                await context.send("responde a un mensaje para dar contexto")
                return

            # Get conversation context from Redis
            quote_ts = context.message.quote.id
            group = context.message.group

            messages = await redis_client.get_messages_since(group, quote_ts)

            # Filter out bot messages and commands
            bot_prefixes = (
                "TL;DR:",
                "!chat",
                "!grok",
                "!grye",
                "!tldr",
                "!help",
                "!groupid",
            )
            messages = [
                msg for msg in messages if not msg["text"].startswith(bot_prefixes)
            ]

            if not messages:
                # Fallback: just use the quoted message
                conversation = f"- {context.message.quote.text}"
            else:
                # Format conversation
                conversation = "\n".join(f"- {msg['text']}" for msg in messages)

        # Build prompt from encrypted templates
        prompts = get_prompts()
        template = prompts["chat"].get(mode, prompts["chat"]["chat"])
        prompt = template.format(conversation=conversation)

        # Call Groq
        try:
            response = await self.groq.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
            )
            answer = response.choices[0].message.content
            if mode == "tldr":
                answer = f"TL;DR: {answer}"
            if mode == "grye":
                await context.send(answer)
            else:
                await context.reply(answer)
        except RateLimitError:
            await self._send_rate_limited(context)
        except Exception as e:
            await context.send(f"error con groq: {e}")
