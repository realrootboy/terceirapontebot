import web
urls = (
'/input', 'index'
)
class index:
    def GET(self):
        i = web.input(name=None)
        return render.index(i.name)
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

render = web.template.render('templates/')

# IMPORTS
from telegram.ext import Updater, CommandHandler
from configparser import ConfigParser
from bs4 import BeautifulSoup
import requests
import os

# CONFIG SETUP
config = ConfigParser()
config.read('config.ini')

headers = {'user-agent': 'Mozilla/5.0'}

# CREDENTIALS
token = config.get('access', 'token')

# CONFIG TELEGRAM
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

# BOT MESSAGES
welcome = "Seja bem-vindo ao Terceira Ponte Bot! @realrootboy"

# BOT FUNCTIONS AND HANDLERS


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome)


def agora(update, context):
    html = requests.get("https://www.rodosol.com.br/#", headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')

    for link in soup.find_all('a', class_="imagem", rel="prettyPhoto[TP]"):
        context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=link.get('href'))


start_handler = CommandHandler('start', start)
agora_handler = CommandHandler('agora', agora)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(agora_handler)

# POOL
updater.start_polling()
