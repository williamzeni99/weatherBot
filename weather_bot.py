import telegram
from telegram import KeyboardButton, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

import weather_module as w

TOKEN = "5173123971:AAEPHhg-YIIlLPvOquLDEt7MM_-6k0Ndy5Q"

# How many times it checks the weather in seconds
INTERVAL = 15


def echo(update: Updater, context: CallbackContext, message: str):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def getcityname_id(args):
    cityname = ""
    cityid = ""
    for x in args:
        cityid += x.lower()
        cityid += "_"
        cityname += x
        cityname += " "

    return {"cityname": cityname, "cityid": cityid}


def callback_timer(context: CallbackContext):
    # context.bot.send_message(chat_id=context.job.context.effective_chat.id, text='One message every minute')
    update = context.job.context.get("update")
    city = context.job.context.get("city")
    try:
        coordinates = w.get_coordinates(city)
        meteodata = w.get_weather_data(coordinates)
        if w.is_critical(meteodata):
            echo(update, context, w.print_weather_data(meteodata))

    except Exception as e:
        echo(update, context, str(e))


# job name prototype= chatId_City (1234_vedano_al_lambro)
def getNotify(update: Update, context: CallbackContext):
    if len(context.args) > 0:
        citydata = getcityname_id(context.args)

        try:
            w.get_coordinates(citydata.get("cityname"))
        except Exception as e:
            echo(update, context, str(e))
            return

        j = context.job_queue
        chat_id = str(update.effective_chat.id) + "_" + citydata.get("cityid")

        if not j.get_jobs_by_name(chat_id):
            j.run_repeating(callback_timer, interval=INTERVAL,
                            context={"update": update, "city": citydata.get("cityname")},
                            name=chat_id)
            echo(update, context, "Notifica impostata")
        else:
            echo(update, context, "Notifica già impostata")
    else:
        echo(update, context, "Parametro mancante: usa il comando /get_alert seguito dal nome di una città")


def stopCommand(update: Update, context: CallbackContext):
    j = context.job_queue
    if len(context.args) > 0:
        citydata = getcityname_id(context.args)

        chat_id = str(update.effective_chat.id) + "_" + citydata.get("cityid")

        if len(j.get_jobs_by_name(chat_id)) == 0:
            echo(update, context, f"Nessuna notifica attiva trovata per {citydata.get('cityname')}")
            return

        for x in j.get_jobs_by_name(chat_id):
            x.schedule_removal()

    else:
        chat_id = str(update.effective_chat.id)
        jobs = list(j.jobs())
        for x in jobs:
            name = x.name
            name = name.split("_")[0]
            if name != chat_id:
                jobs.remove(x)

        if len(jobs) == 0:
            echo(update, context, "Nessuna notifica attiva trovata")
            return

        for x in jobs:
            x.schedule_removal()

    echo(update, context, "Notifiche disattivate correttamente")


# /start
def startCommand(update: Updater, context: CallbackContext):
    introtext = "Benvenuto!\n" \
                "Questo bot serve per ricevere 'assistenza meteo'. Invia il nome di una città o la tua posizione e ti " \
                "verranno mandate le info meteo di quel luogo. \n\n" \
                "Se invece vuoi ricevere notifiche meteo di allerta digita /get_alert Nome-Città  \n" \
                "Puoi ricevere notifiche di più città con lo stesso comando.\n\n" \
                "Puoi terminare di ricevere le notifiche di una città specifica con /stop Nome-Città \n" \
                "oppure disattivare tutte le notifiche con /stop \n\n" \
                "Per avere una panoramica delle notifiche attive usa il comando /list "

    buttons = [[KeyboardButton("Invia posizione attuale", request_location=True)]]
    reply_markup = telegram.ReplyKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=introtext,
                             reply_markup=reply_markup)


def listCommand(update: Update, context: CallbackContext):
    j = context.job_queue
    text = "Notiche attive\n\n"
    chat_id = str(update.effective_chat.id)
    jobs = list(j.jobs())
    for x in jobs:
        name = x.name
        name = name.split("_")[0]
        if name != chat_id:
            jobs.remove(x)

    if len(jobs) == 0:
        echo(update, context, "Nessuna notifica attiva trovata")
        return

    for x in jobs:
        name = x.name.split("_")
        name.remove(name[0])
        name = " ".join(name)
        text += " - " + name + "\n"

    text += "\n"

    echo(update, context, text)


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
        CommandHandler('get_alert', getNotify),
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
