from signalbot import SignalBot

from app import config
from app.cmds import ALL_COMMANDS


def main():
    if not config.PHONE_NUMBER:
        print("ERROR: Set PHONE_NUMBER in .env")
        return

    bot = SignalBot(
        {
            "signal_service": config.SIGNAL_SERVICE,
            "phone_number": config.PHONE_NUMBER,
        }
    )

    for cmd in ALL_COMMANDS:
        bot.register(cmd)

    masked = config.PHONE_NUMBER[:-2] + "xx"
    print(f"Bot started with {masked}")
    bot.start()


if __name__ == "__main__":
    main()
