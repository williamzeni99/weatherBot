import telegram
from telegram import Bot, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

import weather_module as w


TOKEN = "5173123971:AAEPHhg-YIIlLPvOquLDEt7MM_-6k0Ndy5Q"

bot = Bot(TOKEN)
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue

instantlocText = "Posizione Attuale"
coordinatesText = "Posizione manuale"
notifyText = "Notifica Meteo"


def echo(update: Updater, context: CallbackContext, message: str):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# /start
def startCommand(update: Updater, context: CallbackContext):
    buttons = [[KeyboardButton(instantlocText, request_location=True)], [KeyboardButton(coordinatesText)]]
    reply_markup = telegram.ReplyKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Benvenuto! Seleziona una delle due opzioni. Ti invieremo il meteo attuale',
                             reply_markup=reply_markup)


def locationHandler(update: Updater, context: CallbackContext):
    location = update.message.location
    coordinates = [location.latitude, location.longitude]
    try:
        data = w.get_weather_data(coordinates)
        echo(update, context, w.print_weather_data(data))
    except Exception as e:
        echo(update, context, str(e))


def manuallocationHandler(update: Updater, context: CallbackContext):
    if coordinatesText in update.message.text :
        text="Inserisci il nome di una città"
        echo(update, context, text)
    else:
        city = update.message.text
        try:
            coordinates = w.get_coordinates(city)
            meteodata = w.get_weather_data(coordinates)
            echo(update, context, w.print_weather_data(meteodata))
        except Exception as e:
            echo(update, context, str(e))


def main():
    start_handler = CommandHandler('start', startCommand)
    location_handler = MessageHandler(Filters.location, locationHandler)
    manual_location_handler = MessageHandler(Filters.text, manuallocationHandler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(location_handler)
    dispatcher.add_handler(manual_location_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
