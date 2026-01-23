from .help import HelpCommand
from .groupid import GroupIdCommand
from .cache import MessageCacheCommand
from .chat import ChatCommand
from .triggers import TriggerCommand

ALL_COMMANDS = [
    MessageCacheCommand(),  # Must be first to cache all messages
    HelpCommand(),
    GroupIdCommand(),
    ChatCommand(),
    TriggerCommand(),
]
