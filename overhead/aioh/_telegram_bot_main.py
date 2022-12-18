import Demos.service.serviceEvents

# from telegram.helpers import Update, Message, MessageType, Union, Optional

from codex_class import CodexSmall, ChatHelpers

from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Chat
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import ChatMember, ChatMemberLeft, ChatMemberMember, ChatMemberAdministrator
from telegram.ext import DictPersistence, Defaults, ApplicationBuilder, Application
from telegram.error import BadRequest, TimedOut, NetworkError
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, CallbackContext
import logging
from telegram.constants import ParseMode, ChatMemberStatus, ChatType, ChatID, ChatAction, BotCommandScopeType
import os
import sys
import time
import json
import requests
import re
import datetime
import traceback
import threading
import queue
import random
import string
import base64
import hashlib
import hmac

import urllib.parse
import urllib.request
import urllib.error

import aiohttp
import asyncio

from typing import NoReturn, List, Dict, Tuple, Union, Optional, Any, Callable, Awaitable, TypeVar, Generic, cast, overload
import requests as req
from aiohttp import web

# Path: overhead\aioh\_telegram_bot_main.py
# Fuse this snippet from overhead\aioh\telegram_kerttulibot.py with base telegram bot code

# from telegram import __version__ as TG_VER
# from codex_class import ChatBotsTalking
#
# # from telegram import __version_info__
#
# # except ImportError:
# #     __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]  # type: ignore[assignment]
#
# # if __version_info__ < (20, 0, 0, "alpha", 1):
# #     raise RuntimeError(
# #         f"This example is not compatible with your current PTB version {TG_VER}. To view the "
# #         f"{TG_VER} version of this example, "
# #         f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
# #     )
#
#



#
# class ChatBotsTalking:
#     def __init__(self, starter=None, definition=None, continuous_save=True, overwrite=False):
#
#         TOKEN = TOKEN_KERTTULIBOT
#
#         self.options_text = None
#
#         self.command_list = None
#         self.subject_1_name = None
#         self.subject_2_name = None
#
#         self.starter = starter
#         self.definition = definition
#         self.overwrite = overwrite
#         self.continuous_save = continuous_save
#
#         self.helper = ChatHelpers(starter, definition, continuous_save, overwrite)
#         self.helper.subject_1_name, self.helper.subject_2_name = self.subject_1_name, self.subject_2_name
#         self.helper.chat_init_string(self.starter, self.definition, self.subject_1_name, self.subject_2_name)
#         self.kerttulibot = CodexSmall(engine="code-davinci-002", temperature=0.92, max_tokens=128, top_p=1,
#                                         stop_str="\n", frequency_penalty=0.15, presence_penalty=0.02)
#
#         self.bot1 = InputTextMessageContent(self.kerttulibot.completion(self.helper.conversation, 1))
#
#         self.updater = Updater()
#         self.dispatcher = self.updater.bot.getChat
#
#         self.dispatcher.add_handler(CommandHandler("start", self.start))
#         self.dispatcher.add_handler(CommandHandler("help", self.help))
#         self.dispatcher.add_handler(CommandHandler("commands", self.commands))
#         self.dispatcher.add_handler(CommandHandler("stats", self.stats))
#         self.dispatcher.add_handler(CommandHandler("exit", self.exit))
#         self.dispatcher.add_handler(CommandHandler("set_definition", self.set_definition))
#         self.dispatcher.add_handler(CommandHandler("parameters", self.parameters))
#         self.dispatcher.add_handler(MessageHandler(None, self.wait_user_input))
#
#         self.dispatcher.start_polling()
#         self.dispatcher.idle()
#
#     def start(self, update, context):
#         update.message.reply_text(self.options())
#
#     def help(self, update, context):
#         update.message.reply_text(self.options())
#
#     def commands(self, update, context):
#         update.message.reply_text(self.options())
#
#     def stats(self, update, context):
#         update.message.reply_text(self.helper.conversation_info())
#
#     def exit(self, update, context):
#         update.message.reply_text("Exiting")
#         self.updater.stop()
#         sys.exit()
#
#     def set_definition(self, update, context):
#         self.helper.set_definition(context)
#         update.message.reply_text(self.definition)
#
#     def parameters(self, update, context):
#         update.message.reply_text(self.options())
#
#     def options(self):
#         self.options_text = f"""
#         Commands:
#         /start - Start the bot
#         /help - Help
#         /commands - List of commands
#         /stats - Show conversation stats
#         /exit - Exit the bot
#         /set_definition - Set the definition
#         /parameters - Show parameters
#         """
#         return self.options_text
#
#     def change_parameters(self, bot):
#         bot.temperature = float(input("Temperature: "))
#         bot.max_tokens = int(input("Max tokens: "))
#         bot.top_p = float(input("Top p: "))
#         bot.stop_str = input("Stop string: ")
#         bot.frequency_penalty = float(input("Frequency penalty: "))
#         bot.presence_penalty = float(input("Presence penalty: "))
#         # this needs to be set interactively from group chat
#
#
#     def wait_user_input(self, update, context):
#         self..wait_user_input(update, context)
#         update.message.reply_text(self.helper.conversation_info())
#
#