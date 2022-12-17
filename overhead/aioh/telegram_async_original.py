#!/usr/bin/env python
# pylint: disable=wrong-import-position
"""Simple Bot to reply to Telegram messages.

This is built on the API wrapper, see echobot.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""

import asyncio
import logging
import os
import pathlib
from pathlib import Path
import random
import time
import typing

from typing import NoReturn

import telegram.constants
from telegram import Bot
from telegram.error import Forbidden, NetworkError

# from telegram import __version__ as TG_VER
from telegram_kerttulibot import ChatBotsTalking
from _telegram_bots import _kerttulibot


# from telegram import __version_info__

# except ImportError:
#     __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]  # type: ignore[assignment]

# if __version_info__ < (20, 0, 0, "alpha", 1):
#     raise RuntimeError(
#         f"This example is not compatible with your current PTB version {TG_VER}. To view the "
#         f"{TG_VER} version of this example, "
#         f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
#     )


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

chatbot = ChatBotsTalking(starter=None, definition=None, continuous_save=True, overwrite=False)
chatbot.helper.load_conversation_file("kerttulibot_chatroom_1.txt")
chatbot.subject_1_name = "kerttulibot"
chatbot.subject_2_name = "group_chat"
chatbot.bot2human_async()

id_counter = 0
update_id_mem = 0


# need path to the token file in user PATH VAR
async def echo(bot: Bot, update_id: typing.Optional[int]) -> int:
	"""Echo the message the user sent."""
	global id_counter
	global update_id_mem
	global chatbot
	# Request updates after the last update_id
	for update in await bot.get_updates(offset=update_id, timeout=10):
		zippupdate_id = update.update_id + 1
		
		if update.message:  # your bot can receive updates without messages
			# Reply to the message
			if update.message.text:
				if update.message.text == "/start":
					await update.message.reply_text("Hi!")
				else:
					await update.message.reply_text(update.message.text)
			else:
				await update.message.reply_text("I don't understand you.")
	return update_id


# kerttulibot = os.path.join(Path(__file__).parent, "kerttulibot_token.txt")
# print(kerttulibot)
# TOKEN = TOKEN_KERTTULIBOT


async def main() -> NoReturn:
	"""Run the bot."""
	# Create the EventHandler and pass it your bot's token.
	# Here we use the `async with` syntax to properly initialize and shutdown resources.

	async with Bot(_kerttulibot.TOKEN) as bot:
		# get the first pending update_id, this is so we can skip over it in case
		# we get a "Forbidden" exception.
		try:
			update_id = (await bot.get_updates())[0].update_id
			update_id += 1
		except IndexError:
			update_id = None
		
		logger.info("listening for new messages...")
		
		while True:
			try:
				
				update_id = await echo(bot, update_id)
			except NetworkError:
				await asyncio.sleep(1)
			except Forbidden:
				# The user has removed or blocked the bot.
				update_id += 1


async def echo(bot: Bot, update_id: int) -> int:
	"""Echo the message the user sent."""
	# Request updates after the last update_id
	updates: List[Update] = await bot.get_updates(offset=update_id, timeout=10)
	
	for update in updates:
		next_update_id = update.update_id + 1
		logger.info("update_id: %s", update_id)
		# Reply to the message
		# if update.message:
		#     chat_id = update.message.chat.id
		#     if chat_id and id_counter == 0:
		#         logger.info("Chat id: %s", chat_id)
		#         # await bot.send_message(chat_id=chat_id, text=chatbot.helper.definition,
		#         #                        allow_sending_without_reply=True)
		#         print("Send messages to chat id: %s", chat_id, "in function echo")
		#         logger.info("Chat id: %s", chat_id)
		#
		#         id_counter += 1
		
		# your bot can receive updates without messages
		# and not all messages contain text
		
		logger.info("Listing all updates: %s", list(updates)[-1])
		
		if update.message and update.message.text:
			# Reply to the message
			
			# await update.message.text
			chatbot.wait_user_input(update)
			logger.info("Found message %s!", update.message.text)
			
			if update.message.text in chatbot.command_list:
				c = chatbot.options(comment=update.message.text)
				# time.sleep(2)
				await update.message.reply_text(c, allow_sending_without_reply=True)
				logger.info("Sent message %s!", c)
				return next_update_id
			
			if "/start" in update.message.text and chatbot.pause_flag:
				c = chatbot.options(comment=update.message.text)
				# time.sleep(2)
				await update.message.reply_text(c, allow_sending_without_reply=True)
				logger.info("Sent message %s!", c)
				chatbot.pause_flag = False
				return next_update_id
			
			if update.message.text in ("/stop", "/pause") and not chatbot.pause_flag:
				c = chatbot.options(comment=update.message.text)
				time.sleep(2)
				await update.message.reply_text(c, allow_sending_without_reply=True)
				logger.info("Sent message %s!", c)
				chatbot.pause_flag = True
				return next_update_id
				brea
			
			# prob = [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3]
			prob = [1, 1, 1, 1, 1, 1, 1]
			n = random.choice(prob)
			print("choice: ", n)
			
			if (n == 0 or chatbot.pause_flag is True) and ("@kerttulibot" not in update.message.text):
				return next_update_id
				break
			else:
				for i in range(n):
					time.sleep(10 / n)
					if "groups" in update.message.text and update.message:
						member = telegram.ChatMember(update.message.chat_id, update.message.from_user.id)
						chatbot.helper.conversation += f"\n{member}\n"
						return next_update_id
					elif update.message.text is not None:
						answer = chatbot.answer_user_input(update)
						if "@" in answer:
							await update.message.reply_text(answer)
							return next_update_id
						else:
							await bot.send_message(chat_id=update.message.chat_id, text=answer)
						logger.info("Sent message %s!",answer)
						return next_update_id
						
						# how to prevent looping?
						if answer in chatbot.command_list and next_update_id is update.update_id:
							rint(str(update_id.user_data))
							self.helper.conversation += f"\n{str(update_id.user_data)}\n"


						c = chatbot.options(comment=answer)+ f'{kerttulibot}: self.helper.conversation += f"\n{str(update_id.user_data)}\n"'
						time.sleep(2)
						await update.message.reply_text(c, allow_sending_without_reply=True)
						logger.info("Sent message %s!", c)
						return next_update_id + 1
					
			return next_update_id + 1
		return next_update_id +1
	return update_id


if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
		pass