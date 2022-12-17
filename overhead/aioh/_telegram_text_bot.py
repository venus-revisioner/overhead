import logging
import signal
import tracemalloc

import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler


TOKEN = os.getenv('TELEGRAM_BOT)'.strip("'")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('Hi!')

def help(update, context):
    update.message.reply_text('Help!')

def echo(update, context):
    update.message.reply_text(update.message.text)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    print(update.effective_chat.id)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("echo", echo))
    # application.add_handler(CommandHandler(filter(__function=text) & ~filter("command", command), filter("echo", echo)))
    # application.add_error_handler(error)

    print(logging.INFO)

    # updater = Update(update_id=Update.message, context=CallbackContext.DEFAULT_TYPE, bot=telegram.Bot(token=TOKEN))
    # print(updater)
    # updater = Update(telegram.Update.get_bot(self=telegram.Bot(token=TOKEN)), update_id)
    # updater.get_bot().request.post('https://api.telegram.org/{'TOKEN'}getMe')
    print(Update.message)
    # updater.request.post(make_request)
    print(application.chat_data.items())
    # print(start_handler.callback)

    application.run_polling()

    tracemalloc.start()
    application.updater.start_polling()
    application.run_polling()

    # application.updater.idle()    # application.run_idle()
    # application.updater.stop()    # application.stop()