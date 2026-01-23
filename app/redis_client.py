import json

import redis.asyncio as redis

from app import config

_client: redis.Redis | None = None


async def get_client() -> redis.Redis:
    """Get or create Redis async client."""
    global _client
    if _client is None:
        _client = redis.from_url(config.REDIS_URI, db=config.REDIS_DB)
    return _client


def _group_key(group_id: str) -> str:
    """Redis key for a group's message cache."""
    return f"messages:{group_id}"


async def cache_message(group_id: str, timestamp: int, text: str, author: str) -> None:
    """Cache a message in the group's sorted set."""
    client = await get_client()
    key = _group_key(group_id)
    message_data = json.dumps({"text": text, "author": author, "ts": timestamp})

    async with client.pipeline() as pipe:
        # Add message to sorted set with timestamp as score
        pipe.zadd(key, {message_data: timestamp})
        # Set/refresh TTL on the key
        pipe.expire(key, config.MESSAGE_CACHE_TTL)
        await pipe.execute()


async def get_messages_since(group_id: str, since_ts: int) -> list[dict]:
    """Get all messages since a timestamp (inclusive)."""
    client = await get_client()
    key = _group_key(group_id)

    # Get all messages with score >= since_ts
    messages_raw = await client.zrangebyscore(key, since_ts, "+inf")

    messages = []
    for msg in messages_raw:
        try:
            data = json.loads(msg)
            messages.append(data)
        except json.JSONDecodeError:
            continue

    return messages
