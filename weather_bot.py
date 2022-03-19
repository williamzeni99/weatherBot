import telegram
from telegram import KeyboardButton, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

import weather_module as w

TOKEN = "5173123971:AAEPHhg-YIIlLPvOquLDEt7MM_-6k0Ndy5Q"


def echo(update: Updater, context: CallbackContext, message: str):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def callback_timer(context: CallbackContext):
    context.bot.send_message(chat_id=context.job.context.effective_chat.id, text='One message every minute')


def getNotify(update: Update, context: CallbackContext):
    j = context.job_queue
    chat_id = str(update.effective_chat.id)
    if not j.get_jobs_by_name(chat_id):
        j.run_repeating(callback_timer, interval=5, context=update, name=chat_id)
        echo(update, context, "Notifica impostata")
    else:
        echo(update, context, "Notifica già impostata")


def stopCommand(update: Update, context: CallbackContext):
    j = context.job_queue
    for x in j.get_jobs_by_name(str(update.effective_chat.id)):
        x.schedule_removal()

    echo(update, context, "Notifica disattivata")


# /start
def startCommand(update: Updater, context: CallbackContext):
    introtext = "Benvenuto!\n" \
                "Questo bot serve per ricevere 'assistenza meteo'. Invia il nome di una città o la tua posizione e ti " \
                "verranno mandate le info meteo di quel luogo. \n\n" \
                "Se invece vuoi ricevere notifiche meteo di allerta digita \get_alert Nome-Città  \n" \
                "Puoi ricevere notifiche di più città con lo stesso comando.\n\n" \
                "Puoi terminare di ricevere le notifiche di una città specifica con \stop Nome-Città \n" \
                "oppure disattivare tutte le notifiche con \stop \n\n" \
                "Per avere una panoramica delle notifiche attive usa il comando \list "

    buttons = [[KeyboardButton("Invia posizione attuale", request_location=True)]]
    reply_markup = telegram.ReplyKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=introtext,
                             reply_markup=reply_markup)


def listCommand(update: Update, context: CallbackContext):
    print("todo")


def locationHandler(update: Updater, context: CallbackContext):
    location = update.message.location
    coordinates = [location.latitude, location.longitude]
    try:
        data = w.get_weather_data(coordinates)
        echo(update, context, w.print_weather_data(data))
    except Exception as e:
        echo(update, context, str(e))


def manuallocationHandler(update: Updater, context: CallbackContext):
    city = update.message.text
    try:
        coordinates = w.get_coordinates(city)
        meteodata = w.get_weather_data(coordinates)
        echo(update, context, w.print_weather_data(meteodata))
    except Exception as e:
        echo(update, context, str(e))


def main():
    handlers = [
        CommandHandler('start', startCommand),
        CommandHandler('get_notify', getNotify),
        CommandHandler('stop', stopCommand),
        CommandHandler('list', listCommand),

        MessageHandler(Filters.location, locationHandler),
        MessageHandler(Filters.text, manuallocationHandler)
    ]

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    for x in handlers:
        dispatcher.add_handler(x)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
