import asyncio
import sys
import time
from asyncio.log import logger

import telegram
from telegram import Bot
from telegram import Chat
from telegram.error import Forbidden
from telegram.error import NetworkError
from telegram.ext import Updater, CommandHandler, MessageHandler
import logging
from logging .handlers import RotatingFileHandler
import os
import typing

from telegram import Bot, Chat
from overhead.aioh.codex_class import ChatBotsTalking


global id_counter
global update_id_mem
global id_counter
global update_id_mem
global chatbot

chatbot = ChatBotsTalking(starter=None, definition=None, continuous_save=True, overwrite=False)
chatbot.helper.load_conversation_file("kerttulibot_chatroom_1.txt")
chatbot.subject_1_name = "kerttulibot"
chatbot.subject_2_name = "group_chat"
chatbot.bot2human_async()




sys.path_hooks.append(lambda path: path.replace(" ", "_"))
TOKEN = os.path.append(os.environ["TELEGRAM_BOT_TOKEN"])
print("try no 1", TOKEN)
# TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
# print("try no 2", TOKEN)
# updater = Updater(os.environ["TELEGRAM_BOT_TOKEN"])
# print("starting")


def main_async(update, update_id):
	pass


main_async(update=None, update_id=None)
# Path: overhead\aioh\codex_class.py
import os
import time
import asyncio
import time




exit()
bot = Bot()
updater = Updater(TOKEN)



def start(bot: Bot, update: Update) -> NoReturn:
	"""Send a message when the command /start is issued."""
	update.message.reply_text('Hi!')

	
def help_me(bot: Bot, update: Update) -> NoReturn:
	"""Send a message when the command /help is issued."""
	update.message.reply_text('Help!')
	
def error(bot: Bot, update: Update) -> NoReturn:
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, update.error)
	
async def echo(bot: Bot, update_id: typing.Optional[int]) -> int:
	"""Echo the message the user sent."""
	global id_counter, update
	global update_id_mem
	global chatbot
	
	updater = Updater(os.environ["TELEGRAM_BOT_TOKEN"])
	for update in await updater.bot.get_updates(offset=update_id, timeout=10):
		update_id = main(update, update_id)
		id_counter += 1
		update_id_mem = update_id
		return update_id
	
	# Request updates after the last update_id
	for update in await bot.get_updates(offset=update_id, timeout=10):
		zipupdate_id = update.update_id + 1
		# bot writes first all info of the chatroom, all particcipants, etc.
		# then it writes the stats of the chatroom, like number of messages, etc.
		# then it writes the messages, one by one
		# the messages are written in the following format for human friendly reading:
		# 	[time] [name of the sender] [message count] [list of participants in the chatroom]
		# and highights the most activbe participants in the chatroom
		# the messages are written in the following format for machine friendly reading:
		# 	[time] [name of the sender] [message count] [list of participants in the chatroom]
		
		# if the message is a chatroom info message (not a message from a participant)
		# then we skip it
		
		if update.message.chat.type == "group":
			continue
		else:
			# if the message is from a participant
			# then we add it to the conversation
			# and we send the reply to the participant
			# and we save the conversation
			# and we update the update_id
			chatbot.add_conversation(update.message.text)
			bot.send_message(chat_id=update.message.chat_id, text=chatbot.reply(), disable_notification=True)
			chatbot.save_conversation()
			update_id = zipupdate_id
			return update_id
		
	return updater, update, update_id
	
async def main_chatter() -> typing.NoReturn:
	global chatbot, id_counter, update_id_mem
	"""Start the bot."""
	# Create the EventHandler and pass it your bot's token.

	# Get the dispatcher to register handlers
	updater, update, update_id = echo(bot)
	
	for update in updater.bot.get_updates(offset=update_id, timeout=10):
		update_id = main(update, update_id)
		id_counter += 1
		update_id_mem = update_id
		return update_id
	
	# Request updates after the last update_id
	for update in updater.bot.get_updates(offset=update_id, timeout=10):
	
	# THERE IS NO DISPATCHER IN TELEGRAM.AIO
	# FIND A REPLACEMENT FOR IT !!!!
	
		update.message.reply_text(update.message.text, disable_notification=True)
		# bot listens for users leaving or logging in to the chatroom
		if update.message.left_chat_member is not None:
			chatbot.subject_2_name = update.message.left_chat_member.username
			chatbot.subject_1_name = "kerttulibot"
			chatbot.bot2human_async()
			chatbot.subject_2_name = "group_chat"
			chatbot.subject_1_name = update.message.left_chat_member.username
			chatbot.bot2human_async()
		elif update.message.new_chat_members is not None:
			chatbot.subject_2_name = update.message.new_chat_members[0].username
			chatbot.subject_1_name = "kerttulibot"
			chatbot.bot2human_async()
			chatbot.subject_2_name = "group_chat"
			chatbot.subject_1_name = update.message.new_chat_members[0].username
			chatbot.bot2human_async()
			# bot listens for messages
		elif update.message.text is not None:
			chatbot.subject_2_name = "group_chat"
			chatbot.subject_1_name = update.message.from_user.username
			chatbot.bot2human_async()
			chatbot.subject_2_name = update.message.from_user.username
			chatbot.subject_1_name = "kerttulibot"
			chatbot.bot2human_async()
		if update.message:  # your bot can receive updates without messages
		# Reply to the message
			if update.message.text:
				if update.message.text == "/start":
					await update.message.reply_text("Hi!", disable_notification=True)
				else:
					await update.message.reply_text(update.message.text, disable_notification=True)
					chatbot.subject_1_input = update.message.text
					chatbot.subject_2_input = update.message.text
					chatbot.human2bot_async()
				await update.message.reply_text(chatbot.subject_1_output, disable_notification=True)
				await update.message.reply_text(chatbot.subject_2_output, disable_notification=True)
				chatbot.helper.save_conversation_file("kerttulibot_chatroom_1.txt")
			# Reply to the message
			update.message.reply_text(update.message.text)
			
		# update_id is used to keep track of the last update received
		update_id = update.update_id + 1
		
		id_counter += 1
		

def main(update: Update, update_id: typing.Optional[int]) -> int:
	global chatbot, id_counter, update_id_mem
	"""Start the bot."""
	chat = Chat()
	# Create the EventHandler and pass it your bot's token.
	chat.updater = Updater(os.environ["TELEGRAM_BOT_TOKEN"])
	# Get the dispatcher to register handlers
	chat.dispatcher = chat.updater.dispatcher
	# bot listens for users leaving or logging in to the chatroom
	if update.message.left_chat_member is not None:
		chatbot.subject_2_name = update.message.left_chat_member.username
		chatbot.subject_1_name = "kerttulibot"
		chatbot.bot2human_async()
		chatbot.subject_2_name = "group_chat"
		chatbot.subject_1_name = update.message.left_chat_member.username
		chatbot.bot2human_async()
	elif update.message.new_chat_members is not None:
		chatbot.subject_2_name = update.message.new_chat_members[0].username
		chatbot.subject_1_name = "kerttulibot"
		chatbot.bot2human_async()
		chatbot.subject_2_name = "group_chat"
		chatbot.subject_1_name = update.message.new_chat_members[0].username
		chatbot.bot2human_async()
	# bot listens for messages
	elif update.message.text is not None:
		chatbot.subject_2_name = "group_chat"
		chatbot.subject_1_name = update.message.from_user.username
		chatbot.bot2human_async()
		chatbot.subject_2_name = update.message.from_user.username
		chatbot.subject_1_name = "kerttulibot"
		chatbot.bot2human_async()
	if update.message:  # your bot can receive updates without messages
		# Reply to the message
		if update.message.text:
			if update.message.text == "/start":
				update.message.reply_text("Hi!")
			else:
				update.message.reply_text(update.message.text)
				chatbot.subject_1_input = update.message.text
				chatbot.subject_2_input = update.message.text
				chatbot.human2bot_async()
				update.message.reply_text(chatbot.subject_1_output)
				update.message.reply_text(chatbot.subject_2_output)
				chatbot.helper.save_conversation_file("kerttulibot_chatroom_1.txt")
				
	# Reply to the message
	update.message.reply_text(update.message.text)
	
	# update_id is used to keep track of the last update received
	update_id = update.update_id + 1
	
	id_counter += 1
	
	update_id_mem = update_id
	
	return update_id
	
def main_async(update: Update, update_id: typing.Optional[int]) -> int:
	global chatbot, id_counter, update_id_mem
	"""Start the bot."""
	chat = Chat()
	# Create the EventHandler and pass it your bot's token.
	chat.updater = Updater(os.environ["TELEGRAM_BOT_TOKEN"])
	# Get the dispatcher to register handlers
	chat.dispatcher = chat.updater.dispatcher
	# bot listens for users leaving or logging in to the chatroom
	chat.dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, chat.left_chat_member))
	chat.dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, chat.new_chat_members))
	# bot listens for messages
	chat.dispatcher.add_handler(MessageHandler(Filters.text, chat.text))
	
	# Start the Bot
	updater.start_polling()
	
	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	

async def main() -> NoReturn:
	# Create the EventHandler and pass it your bot's token
	while True:
	
	# get the first pending update_id, this is so we can skip over it in case
	# we get a "Forbidden" exception.
	try:
		update_id = await bot.get_updates()[0].update_id
		update_id += 1
	except IndexError:
		update_id = None
		update_id += 1
	
	time.sleep(2)
	logger.info("listening for new messages...")
	
	if update_id:
		update_id = await echo(bot, update_id)
	except NetworkError:
	time.sleep(1)

	except Forbidden:
	# The user has removed or blocked the bot.
	update_id += 1


if __name__ == "__main__":
	asyncio.run(main())