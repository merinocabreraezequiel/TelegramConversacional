import asyncio
import telegram
import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, Updater
import math
from unidecode import unidecode
import random

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

gd = None

def loadconfig():
    f = open("env.json", encoding='utf-8-sig')
    string_double_quotes = f.read()
    return(json.loads(string_double_quotes))

def loadGD():
    f = open("objects/map.json", encoding='utf-8-sig')
    string_double_quotes = f.read()
    print(string_double_quotes)
    return(json.loads(string_double_quotes))

async def main(conf):
    bot = telegram.Bot(str(conf['BOT_TOKEN']))
    async with bot:
        #print(await bot.get_me())
        #print((await bot.get_updates())[0])
        await bot.send_message(text=bot.username, chat_id=bot.id)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hola "+update.effective_chat.username+", soy un bot preprandome para hacerte pasar una aventura conversacional\nEjecuta /comandos para conocer tus opciones.\n\n<b>Empieza la aventura</b>\n"+gd["room"]["View"]+"\n"+gd["room"]["Desc"],parse_mode='html')

async def coger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    returntxt = ' '.join(context.args)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="coges el "+returntxt)
async def imagen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=r'.\\img\\01.jpg')

async def comandos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""/n: te mueves al norte
s: te mueves al sur
e: te mueves al este
o: te mueves al oeste
mirar: observas a tu alrededor, puedes indicar objeto
coger: recoges el objeto indicado
abrir: abres un objeto
cerrar: cierras un objeto
usar: usas un objeto
""")

async def pitagoras(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 3:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Introduce el comando con el siguiente formato /pitagoras 'valorA' 'valorB', los decimales son con '.'")
    else:
        if not (context.args[0]).isnumeric():
            try:
                argA = float(context.args[0])
            except ValueError:
                if context.args[0] == "x":
                    argA = context.args[0]
                else:
                    argA = None
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="La Cateto A ha de ser un numero o un float")
        else:
            argA = float(context.args[0])

        if not (context.args[1]).isnumeric():
            try:
                argB = float(context.args[1])
            except ValueError:
                if context.args[1] == "x":
                    argB = context.args[1]
                else:
                    argB = None
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="La Cateto B ha de ser un numero o un float")
        else:
            argB = float(context.args[1])

        if not (context.args[2]).isnumeric():
            try:
                argH = float(context.args[2])
            except ValueError:
                if context.args[2] == "x":
                    argH = context.args[2]
                else:
                    argH = None
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="La Hipotenusa ha de ser un numero o un float")
        else:
            argH = float(context.args[2])

        if not (argA is None) and not (argB is None) and not (argH is None):
            if argA == "x":
                argA = math.sqrt(argH**2 - argB**2)
            else:
                if argB == "x":
                    argB = math.sqrt(argH**2 - argA**2)
                else:
                    argH=math.sqrt((argA**2)+(argB**2))
            await context.bot.send_message(chat_id=update.effective_chat.id, text="La resolución del triangulo es:\nCateto A: "+str(argA)+"\nCateto B: "+str(argB)+"\nHipotenusa: "+str(argH))

async def bola(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Me tienes que hacer alguna pregunta")
    else:
        await context.bot.send_animation(chat_id=update.effective_chat.id, animation=r'.\\img\\bola8p.gif')
        r = random.randint(1,8)
        if r == 1:
           resp = "Sí, definitivamente sí."
        elif r == 2:
           resp = "Absolutamente."
        elif r == 3:
            resp = "Sin duda."
        elif r == 4:
            resp = "La respuesta es complicada."
        elif r == 5:
            resp = "Preguntame otra vez más tarde."
        elif r == 6:
            resp = "Mejor no te lo digo."
        elif r == 7:
            resp = "Mis fuentes dicen que no."
        else:
            resp = "Lo dudo mucho."
    await context.bot.send_message(chat_id=update.effective_chat.id, text="A tu pregunta te puedo decir que:\n"+resp)


async def textProcesor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Te lo devuelvo: "+update.message.text)


def normalize_command(command):
    commandSplit = command.split()
    normalized_command = unidecode(commandSplit[0])
    return normalized_command.casefold()

if __name__ == '__main__':
    #asyncio.run(main(loadconfig()))
    conf = loadconfig()
    gd = loadGD()
    application = ApplicationBuilder().token(str(conf['BOT_TOKEN'])).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    coger_handler = CommandHandler('coger', coger)
    application.add_handler(coger_handler)

    imagen_handler = CommandHandler('mapa', imagen)
    application.add_handler(imagen_handler)

    comandos_handler = CommandHandler('comandos', comandos)
    application.add_handler(comandos_handler)

    pitagoras_handler = CommandHandler(normalize_command("pitagoras"), pitagoras)
    application.add_handler(pitagoras_handler)

    bola_handler = CommandHandler('bola8', bola)
    application.add_handler(bola_handler)

    genText_handler = MessageHandler(filters.Text(), textProcesor)
    application.add_handler(genText_handler)

    application.run_polling()