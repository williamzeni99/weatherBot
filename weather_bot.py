import telegram
from telegram import Bot, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext

import weather_module as w

TOKEN = "5173123971:AAEPHhg-YIIlLPvOquLDEt7MM_-6k0Ndy5Q"

bot = Bot(TOKEN)
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue


def echo(update: Updater, context: CallbackContext, message: str):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# /start
def startCommand(update: Updater, context: CallbackContext):
    buttons = [[KeyboardButton("Posizione Attuale")], [KeyboardButton("Posizione manuale")]]
    reply_markup = telegram.ReplyKeyboardMarkup(buttons)
    # reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('Share Location Info', request_location=True)]])
    context.bot.send_message(chat_id=update.effective_chat.id, text='Benvenuto! Seleziona una delle due opzioni', reply_markup=reply_markup)


def getmeteo(update: Updater, context: CallbackContext):

    if len(update.message.text.split(' ')) < 2:
        mex = "Parameter is missing. Please insert a city name."
        echo(update, context, mex)
        return
    city = update.message.text.split(' ')[1]

    try:
        meteodata = w.get_weather_data(city)
        echo(update, context, w.print_weather_data(meteodata))
    except Exception as e:
        echo(update, context, str(e))


def main():
    meteo_handler = CommandHandler('getmeteo', getmeteo)
    start_handler = CommandHandler('start', startCommand)
    dispatcher.add_handler(meteo_handler)
    dispatcher.add_handler(start_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
