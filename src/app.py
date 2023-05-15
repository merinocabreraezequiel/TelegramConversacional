import asyncio
import telegram
import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, Updater
import math

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def loadconfig():
    f = open("env.json", "r")
    string_double_quotes = f.read()
    return(json.loads(string_double_quotes))

async def main(conf):
    bot = telegram.Bot(str(conf['BOT_TOKEN']))
    async with bot:
        #print(await bot.get_me())
        #print((await bot.get_updates())[0])
        await bot.send_message(text=bot.username, chat_id=bot.id)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hola "+update.effective_chat.username +", soy un bot preprandome para hacerte pasar una aventura conversacional\nEjecuta /comandos para conocer tus opciones.")

async def norte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Te mueves al norte")
async def sur(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Te mueves al sur")
async def este(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Te mueves al este")
async def oeste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Te mueves al oeste")
async def coger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    returntxt = ' '.join(context.args)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="coges el "+returntxt)
async def imagen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=r'.\\img\\01.jpg')

async def comandos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""/norte: te mueves al norte
/sur: te mueves al sur
/este: te mueves al este
/oeste: te mueves al oeste
/mirar: observas a tu alrededor, puedes indicar objeto
/coger: recoges el objeto indicado
""")

async def pitagoras(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Introduce el comando con el siguiente formato /pitagoras 'valorA' 'valorB', los decimales son con '.'")
    else:
        if not (context.args[0]).isnumeric():
            try:
                argA = float(context.args[0])
            except ValueError:
                argA = None
                await context.bot.send_message(chat_id=update.effective_chat.id, text="La variable 'valorA' ha de ser un numero o un float")
        else:
            argA = float(context.args[0])
        if not (context.args[1]).isnumeric():
            try:
                argB = float(context.args[1])
            except ValueError:
                argB = None
                await context.bot.send_message(chat_id=update.effective_chat.id, text="La variable 'valorB' ha de ser un numero o un float")
        else:
            argB = float(context.args[1])
        if not (argA is None) and not (argB is None):
            hipotenusa=math.sqrt((float(context.args[0])*float(context.args[0]))+(float(context.args[1])*float(context.args[1]) ))
            await context.bot.send_message(chat_id=update.effective_chat.id, text="La hipotenusa es de "+str(hipotenusa))


async def textProcesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

if __name__ == '__main__':
    #asyncio.run(main(loadconfig()))
    conf = loadconfig()
    application = ApplicationBuilder().token(str(conf['BOT_TOKEN'])).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    norte_handler = CommandHandler('norte', norte)
    application.add_handler(norte_handler)
    sur_handler = CommandHandler('sur', sur)
    application.add_handler(sur_handler)
    este_handler = CommandHandler('este', este)
    application.add_handler(este_handler)
    oeste_handler = CommandHandler('oeste', oeste)
    application.add_handler(oeste_handler)
    coger_handler = CommandHandler('coger', coger)
    application.add_handler(coger_handler)

    imagen_handler = CommandHandler('mapa', imagen)
    application.add_handler(imagen_handler)

    comandos_handler = CommandHandler('comandos', comandos)
    application.add_handler(comandos_handler)

    pitagoras_handler = CommandHandler('pitagoras', pitagoras)
    application.add_handler(pitagoras_handler)

    genText_handler = MessageHandler(filters.Text(), textProcesor)
    application.add_handler(genText_handler)

    application.run_polling()