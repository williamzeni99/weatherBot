import telegram
from telegram import *
from telegram.ext import *
from geopy.geocoders import Nominatim

# calling the Nominatim tool
loc = Nominatim(user_agent="GetLoc")


TOKEN = "5173123971:AAEPHhg-YIIlLPvOquLDEt7MM_-6k0Ndy5Q"


#/start
def startCommand(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton("Posizione Attuale")], [KeyboardButton("Posizione manuale")]]
    reply_markup = telegram.ReplyKeyboardMarkup(buttons)
    # reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('Share Location Info', request_location=True)]])
    context.bot.send_message(chat_id=update.effective_chat.id, text='Benvenuto! Seleziona una delle due opzioni', reply_markup=reply_markup)


def messageHandler(update: Update, context: CallbackContext):
    location = context.location
    address = loc.reverse((location.latitude, location.logitude))
    update.message.reply_text(f'Location address: {address}')


def main():
    upd = Updater(TOKEN)
    disp = upd.dispatcher

    #upd.message.reply_text('Benvenuto! Seleziona una delle due opzioni')

    disp.add_handler(CommandHandler("start", startCommand))
    disp.add_handler(MessageHandler(Filters.location, messageHandler))

    upd.start_polling()

    upd.idle()


if __name__ == '__main__':
    main()

