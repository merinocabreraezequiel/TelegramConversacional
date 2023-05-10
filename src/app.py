import asyncio
import telegram
import json

def loadconfig():
    f = open("env.json", "r")
    string_double_quotes = f.read()
    return(json.loads(string_double_quotes))

async def main(conf):
    bot = telegram.Bot(str(conf['BOT_TOKEN']))
    async with bot:
        print(await bot.get_me())


if __name__ == '__main__':
    asyncio.run(main(loadconfig()))