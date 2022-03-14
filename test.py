from telegram import Bot, InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import CommandHandler, Updater, CallbackContext, MessageHandler, Filters, InlineQueryHandler
import logging
import requests
import json
from datetime import datetime

TOKEN = '5173123971:AAEPHhg-YIIlLPvOquLDEt7MM_-6k0Ndy5Q'

bot = Bot(TOKEN)
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
j=updater.job_queue

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def unknowncmd(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def callback_minute(context: CallbackContext):
    #context.bot.send_message(chat_id='@examplechannel', text='One message every minute')


#job_minute = j.run_repeating(callback_minute, interval=60, first=10)

def inline_caps(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


def echo(update: Updater, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def start(update: Updater, context: CallbackContext):
    context.bot.sendMessage(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def main():
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    unknown_handler = MessageHandler(Filters.command, unknowncmd)

    inline_caps_handler = InlineQueryHandler(inline_caps)
    dispatcher.add_handler(inline_caps_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(unknown_handler)



    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
