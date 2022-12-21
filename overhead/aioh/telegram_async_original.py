#!/usr/bin/env python
# pylint: disable=wrong-import-position
"""Simple Bot to reply to Telegram messages.

This is built on the API wrapper, see echobot.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""

import asyncio
import json
import logging
import queue
import time
from pprint import pprint
from typing import NoReturn

from telegram import Bot
from telegram.error import Forbidden
from telegram.error import NetworkError
from telegram.ext import Updater

from telegram_json import update_json_file, update_json_file_with_update
from _telegram_bots import _kerttulibot
# from telegram import __version__ as TG_VER
from telegram_kerttulibot import ChatBotsTalking

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

banned_chats = {'id': -1001805901846, 'title': 'Candyland', 'type': '', 'username': ''}

# --------------------------------------------------------------------------------------------
arg_1 = ['sarcastic', 'starter_6', 1, 0, 1, 'kerttulibot_chatroom_3.txt']
chatbot = ChatBotsTalking(definition=0, starter=0,
                          continuous_save=1, make_init_str=0, timestamp=1,
                          load="kerttulibot_chatroom_3.txt")
chatbot.subject_1_name = "kerttulibot"
chatbot.subject_2_name = "Human"
chatbot.helper.load_conversation_file()
chatbot.helper.limit_paragraph = 140
chatbot.bot2human_async()
chatbot.bot1.temperature = 0.999
chatbot.bot1.tokens = 256
chatbot.bot1.top_p = 1.
chatbot.bot1.stop_str = "\n\n"

bot = Bot(_kerttulibot.TOKEN)

# print(vars(ChatBotsTalking).__init__)


# @threaded_deco
async def func_injection():
	"""Start the bot."""
	# while True:
	up = await bot.get_updates(timeout=10)
	pup = list(up)
	# pup = str(up).replace("'", '"')
	# pups = "".join(str(pup))
	
	pups = [{k: v for k, v in i.to_dict().items()} for i in pup]
	# pups = '*'.join(pups)
	# update json file
	# pups = decoder.decode(pups)
	if len(pup) > 0:
		print('json file updated')
		json.dump(fp=open("kerttulibot_updates.json", "w", encoding="utf-8"), obj=pups, indent=4, ensure_ascii=False)
	
	# with open("kerttulibot_updates.json", "w") as f:
	# 	json.dump(encoder.raw_decode(pups), f, indent=4)
	# print(pup)
	# with open("kerttulibot_updates.json", "w") as f:
	# 	f.write(json.
	# 	f.close()
	
	# print(pup)
	# print(pup)  # , end="\r")
	await asyncio.sleep(1)

# await func_injection()


async def main() -> NoReturn:
	"""Run the bot."""
	# Create the EventHandler and pass it your bot's token.
	# Here we use the `async with` syntax to properly initialize and shutdown resources.
	# await func_injection()
	me = await bot.get_me()
	# print("I am: ", me)
	async with bot:
		#
		# await bot.set_webhook(_kerttulibot.WEBHOOK_URL)
		
		# get the first pending update_id, this is so we can skip over it in case
		# we get a "Forbidden" exception.
		try:
			update_id = (await bot.get_updates())[1].update_id
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
			logger.info("Found message %s!", update.message.text)
			chatbot.wait_user_input(update)
			
			# if update.message.text in chatbot.command_list:
			# 	c = chatbot.options(comment=update.message.text)
			# 	# time.sleep(2)
			# 	await update.message.reply_text(c, allow_sending_without_reply=False)
			# 	logger.info("Sent message %s!", c)
			# 	return next_update_id-1
			
			# if "/start" in update.message.text and chatbot.pause_flag:
			# 	c = chatbot.options(comment=update.message.text)
			# 	# time.sleep(2)
			# 	await update.message.reply_text(c, allow_sending_without_reply=True)
			# 	logger.info("Sent message %s!", c)
			# 	chatbot.pause_flag = False
			# 	return next_update_id
			
			# if update.message.text in ("/stop", "/pause") and not chatbot.pause_flag:
			# 	c = chatbot.options(comment=update.message.text)
			# 	time.sleep(2)
			# 	user_msg = await update.message.reply_text(c, allow_sending_without_reply=True)
			# 	logger.info("Sent message %s!", c)
			# 	chatbot.pause_flag = True
			# 	return next_update_id
			#
			# prob = [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3]
			# prob = [1, 1, 1, 1, 1, 1, 1]
			# n = random.choice(prob)
			# print("choice: ", n)
			
			# if (n == 0 or chatbot.pause_flag is True) and ("@kerttulibot" not in update.message.text):
			# 	return next_update_id
			# else:
			# 	for i in range(n):
			# 		time.sleep(10 / n)
			
			if update.message.text is not None:
				# update_json_file_with_update(update.message, "kerttulibot_updates.json")
				
				if update.message.chat.title in [*banned_chats.values()]:
					print("Banned chat: ", update.message.to_dict())
					logger.info("Chat %s is banned!", update.message.chat.title)
					print("Chat is banned:, ", update.message.chat.title)
					return next_update_id
				
				else:
					# print("Chat: ", update.message.to_dict())
					answer = ""
					
					if update.message.chat.type == "private":
						await asyncio.sleep(8)
						# get answer from GPT-3
						answer = chatbot.answer_user_input(update)
					
					elif update.message.chat.type == "group":
						await asyncio.sleep(8)
						# get answer from GPT-3
						answer = chatbot.answer_user_input(update)
					
					elif update.message.chat.type == "supergroup":
						await asyncio.sleep(8)
						# get answer from GPT-3
						answer = chatbot.answer_user_input(update)
					
					if "@" in answer:
						await update.message.reply_text(answer, allow_sending_without_reply=True)
						logger.info("Sent reply %s", answer)
					
					if answer != "":
						await bot.send_message(chat_id=update.message.chat_id, text=answer)
						logger.info("Sent message %s", answer)
					
					return next_update_id
			
			else:
				return update_id
		return next_update_id
	return update_id

if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
		pass
