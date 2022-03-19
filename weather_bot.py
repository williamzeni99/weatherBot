from datetime import datetime

import telegram
from telegram import Bot, KeyboardButton, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler, \
    JobQueue, Job

import weather_module as w

TOKEN = "5173123971:AAEPHhg-YIIlLPvOquLDEt7MM_-6k0Ndy5Q"

instantlocText = "Posizione Attuale"
coordinatesText = "Posizione manuale"
notifyText = "Notifica Meteo"


def echo(update: Updater, context: CallbackContext, message: str):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def callback_timer(context: CallbackContext):
    context.bot.send_message(chat_id=context.job.context.effective_chat.id, text='One message every minute')


def startCommand(update: Update, context: CallbackContext):
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
'''def startCommand(update: Updater, context: CallbackContext):
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
'''


def main():
    start_handler = CommandHandler('start', startCommand)
    stop_handler = CommandHandler('stop', stopCommand)
    # location_handler = MessageHandler(Filters.location, locationHandler)
    # manual_location_handler = MessageHandler(Filters.text, manuallocationHandler)
    # dispatcher.add_handler(manual_location_handler)
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(stop_handler)
    # test_handler = CommandHandler('start')
    # dispatcher.add_handler(test_handler)
    # job_que = JobQueue()
    # job_que.set_dispatcher(dispatcher)
    # job_que.run_repeating(callback=testfunc, interval=60)
    # job_que.start()
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
