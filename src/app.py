import asyncio
import telegram
import os


async def main():
    bot = telegram.Bot(os.environ.get('BOT_TOKEN'))
    async with bot:
        print(await bot.get_me())


if __name__ == '__main__':
    asyncio.run(main())