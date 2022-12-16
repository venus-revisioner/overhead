

import telegram
from telegram import Chat
from telegram.ext import ExtBot, CommandHandler, MessageHandler, Filters

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('Hi!')

def help(update, context):
    update.message.reply_text('Help!')

def echo(update, context):
    update.message.reply_text(update.message.text)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    api_key = os.getenv('TELEGRAM_BOT').strip("'")
    user_id = '@talk_channel_for_bot'
    c = Chat(id=5726154361, type="channel", title="talk_channel_for_bot")
    chat_id = "@talk_channel_for_bots"




    method = "getMe"
    make_request = f'https://api.telegram.org/bot{5726154361}:{'TOKEN'}/{method}'
    print(make_request)


    c.id.link(updater.get_updates, context='CHANNEL')
    updater.request.post(make_request)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.dispatcher.add_error_handler(error)
    updater.start_polling()


    commander = CommandHandler("help", help)



    updater.idle()


main()













# create a webhook similar to binance folder in one .py file

# Path: overhead\aioh\telegram_bot_simple.py