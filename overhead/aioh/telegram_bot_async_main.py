

from telegram_kerttulibot import ChatBotsTalking

# These are the imports for all the classes below. They are not needed for the above generalized functions.
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
from telegram import ChatAction, ChatMember, ChatPermissions, ChatPhoto, File, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo, Location, Message, MessageEntity, ParseMode, PhotoSize, ReplyKeyboardMarkup, ReplyKeyboardRemove, Sticker, Update, User, Venue, Video, VideoNote, Voice



class Bot:
	
	def get_bot(self):
		"""Gets the bot."""
		return self.bot

	def get_updater(self):
		"""Gets the updater."""
		return self.updater

	def get_dispatcher(self):
		"""Gets the dispatcher."""
		return self.dispatcher

	def get_job_queue(self):
		"""Gets the job queue."""
		return self.job_queue

	def get_job(self):
		"""Gets the job."""
		return self.job

	def get_message(self):
		"""Gets the message."""
		return self.message

	def get_chat(self):
		"""Gets the chat."""
		return self.chat

	def get_user(self):
		"""Gets the user."""
		return self.user

	def get_chat_member(self):
		"""Gets the chat member."""
		return self.chat_member

	def get_chat_member_updated(self):
		"""Gets the chat member updated."""
		return self.chat_member_updated

	def get_chat_permissions(self):
		"""Gets the chat permissions."""
		return self.chat_permissions

	def get_chat_photo(self):
		"""Gets the chat photo."""
		return self.chat_photo

	def get_master_folder(self):
		"""Gets the master folder."""
		return self.master_folder

	def get_master_file(self):
		"""Gets the master file."""
		return self.master_file

	def get_images_folder(self):
		"""Gets the images folder."""
		return self.images_folder

	def get_images_file(self):
		"""Gets the images file."""
		return self.images_file

	def start(self, bot, update):
		"""Starts the bot."""
		self.bot = bot
		self.updater = updater
		self.dispatcher = dispatcher
		self.job_queue = job_queue
		self.job = job
		self.message = message
		self.chat = chat
		self.user = user
		self.chat_member = chat_member
		self.chat_member_updated = chat_member_updated
		self.chat_permissions = chat_permissions
		self.chat_photo = chat_photo
		self.master_folder = master_folder
		self.master_file = master_file
		self.images_folder = images_folder
		self.images_file = images_file

		# use only wha's necessary for the abofe generalized functions. There is a bijection between the telegram library and modules and the generalized functions.
		# how are these different to above one?


class BotStart(Bot):
	def start(self, bot, update):
		"""Starts the bot."""
		Bot().start(bot, update)
		
		
class BotEcho(Bot):
	def echo(self, bot, update):
		"""Echoes the message."""
		Bot().start(bot, update)
		bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
		
		
class BotEchoPhoto(Bot):
	def echo_photo(self, bot, update):
		"""Echoes the photo."""
		Bot().start(bot, update)
		bot.send_photo(chat_id=update.message.chat_id, photo=update.message.photo[-1].file_id)
		
		
class BotEchoVideo(Bot):
	def echo_video(self, bot, update):
		"""Echoes the video."""
		Bot().start(bot, update)
		bot.send_video(chat_id=update.message.chat_id, video=update.message.video.file_id)
		

class BotEchoVoice(Bot):
	def echo_voice(self, bot, update):
		"""Echoes the voice."""
		Bot().start(bot, update)
		bot.send_voice(chat_id=update.message.chat_id, voice=update.message.voice.file_id)
		
		
class BotEchoDocument(Bot):
	def echo_document(self, bot, update):
		"""Echoes the document."""
		Bot().start(bot, update)
		bot.send_document(chat_id=update.message.chat_id, document=update.message.document.file_id)

# put all different media in a dictionary, and use the same function for all of them. Much more efficient. Also, use the generalized functions above.

def media_library():
	"""Makes the media library."""
	media_library = {}
	media_library["photo"] = {}
	media_library["video"] = {}
	media_library["voice"] = {}
	media_library["document"] = {}
	return media_library

def media_library_add(media_library, media_type, media_id, media_file):
	"""Adds a media to the media library."""
	media_library[media_type][media_id] = media_file

def media_library_get(media_library, media_type, media_id):
	"""Gets a media from the media library."""
	return media_library[media_type][media_id]
# how do you open image, or sound file? use libraries like PIL, or pygame. Also, how do you save them? Use libraries like pickle, or json. Also, how do you get the file id? Use the generalized functions above.

def media_library_save(media_library, media_library_file):
	"""Saves the media library."""
	with open(media_library_file, "w") as file:
		json.dump(media_library, file)
		
def media_library_load(media_library_file):
	"""Loads the media library."""
	with open(media_library_file, "r") as file:
		media_library = json.load(file)
	return media_library

def media_library_delete(media_library, media_type, media_id):
	"""Deletes a media from the media library."""
	del media_library[media_type][media_id]
	
def media_library_delete_all(media_library, media_type):
	"""Deletes all media from the media library."""
	media_library[media_type] = {}
	
	
# Idea is that the bot is capable sending a full photo back, maybe modified, but in large format, like 1920*1080*3
# pixels. Also, the bot is capable of sending a full video back, maybe modified, but in large format, like 1920*1080*3
# this functionality needs to be incorporated into the bot. Also, the bot needs to be able to send a full voice back.
# Through a speech symthesizer, or through a voice changer. Also, the bot needs to be able to send a full document back.
# And send links, convert links, read the content, and comment on it. Also, the bot needs to be able to send a full
# text back, and send links, convert links, read the content, and comment on it.

# But lets start with only one job. Lets try and do the csv file.


class BotEchoCSV(Bot):
	def echo_csv(self, bot, update):
		"""Echoes the csv."""
		Bot().start(bot, update)
		bot.send_document(chat_id=update.message.chat_id, document=open("csv.csv", "rb"))
		
# how do you open a csv file? Use libraries like pandas, or numpy. Also, how do you save them? Use libraries like pickle, or json. Also, how do you get the file id? Use the generalized functions above.
# well, import the best one and use it. Also, how do you send a csv file? Use the generalized functions above..

# libraries:
import pandas as pd
import numpy as np
import json
import pickle
import csv

# functions:
def csv_library():
	"""Makes the csv library."""
	csv_library = {}
	return csv_library

def csv_library_add(csv_library, csv_id, csv_file):
	"""Adds a csv to the csv library."""
	csv_library[csv_id] = csv_file
	
def csv_library_get(csv_library, csv_id):
	"""Gets a csv from the csv library."""
	return csv_library[csv_id]

def csv_library_save(csv_library, csv_library_file):
	"""Saves the csv library."""
	with open(csv_library_file, "w") as file:
		json.dump(csv_library, file)
		
def csv_library_load(csv_library_file):
	"""Loads the csv library."""
	with open(csv_library_file, "r") as file:
		csv_library = json.load(file)
	return csv_library

def csv_library_delete(csv_library, csv_id):
	"""Deletes a csv from the csv library."""
	del csv_library[csv_id]
	
	
	
# Idea is that the bot is capable sending a full csv back, maybe modified, but in large format, like 1920*1080*3


class CSV(Bot):
	def csv(self, bot, update):
		"""Sends a csv."""
		Bot().start(bot, update)
		bot.send_document(chat_id=update.message.chat_id, document=open("csv.csv", "rb"))
		
		# how do you define the job? Use the generalized functions above.. Ok, I want all the jobs excluding media.

	def fill_csv_with_real_data(self):
		"""Fills the csv with real data."""
		# how do you fill the csv with real data? Use libraries like pandas, or numpy. Also, how do you save them? Use libraries like pickle, or json. Also, how do you get the file id? Use the generalized functions above.
		# well, import the best one and use it. Also, how do you send a csv file? Use the generalized functions above..
		# libraries:
		import pandas as pd
		import numpy as np
		import json
		import pickle
		import csv

		# HOW ABOUT MULTIPLE CLASS INHERITANCE? WAY TOO EFFECTIVE!  tRY AGAIN
	

class SuperWorkerBot(BotEchoCSV, CSV):
	def __init__(self):
		"""Initializes the class."""
		pass

	def start(self, bot, update):
		"""Starts the bot."""
		super().start(bot, update)

	def echo_csv(self, bot, update):
		"""Echoes the csv."""
		super().echo_csv(bot, update)
		
	def csv(self, bot, update):
		"""Sends a csv."""
		super().csv(bot, update)
		
	def fill_csv_with_real_data(self):
		"""Fills the csv with real data."""
		super().fill_csv_with_real_data()
		
	def __del__(self):
		"""Deletes the class."""
		super().__del__()
	






# Use superclasses simple functions to create more complex tasks and jobs. Use jobs patcher to delegate the job
# ordering. Make a function that takes a job and a job id, and adds it to the job patcher. Make a function that
# takes a job id, and removes it from the job patcher. Make a function that takes a job id, and returns the job.
# This should be one function.

# Make a function that takes makes a job, and executes it!
# Here is a list of functions for a complete csv bot: csv_fill(), csv_add(), csv_reorder, csv_count_occurences,
# csv_process_data, csv_save(), csv_load(), csv_delete(), csv_send(), csv_send_to_folder(), csv_send_to_group()
# Use two classes in this superclass to connect the dots. First we should make another superclass to conmbine evry
# single telegram class into a superclass. Then we should make another superclass to combine every single csv class
# and general command class. This is the way to go. Also, make a function that takes a job, and executes it. That's it.


def get_some():
	_key_path = "D:\\OVERHEAD_PY\\TOKEN_KERTTULIBOT.txt"
	with open(_key_path, "r") as f:
		_token = f.read()
		_token = _token.strip()
		_token = _token.strip("\n")
		_token = _token.strip("\r")
		_token = _token.strip("\t")
		return _token

chatbot = ChatBotsTalking(starter=None, definition=0, continuous_save=True, overwrite=False)
chatbot.helper.load_conversation_file("kerttulibot_chatroom_1.txt")
chatbot.subject_1_name = "kerttulibot"
chatbot.subject_2_name = "group_chat"
chatbot.bot2human_async()

TOKEN = get_some()
bot = Bot(TOKEN)
updates = bot.get_updates()



class TelegramBot:
	def __init__(self, token: str, chatbot: ChatBotsTalking):

		# GENERAL SETTINGS
		self.token = token
		self.chatbot = chatbot
		self.bot = Bot(self.token)
		self.updates = self.bot.get_updates()
		self.chat_id = self.updates[0].message.chat_id
		self.chat_type = self.updates[0].message.chat.type
		self.chat_title = self.updates[0].message.chat.title
		self.chat_username = self.updates[0].message.chat.username
		self.chat_first_name = self.updates[0].message.chat.first_name
		self.chat_last_name = self.updates[0].message.chat.last_name
		self.chat_all_members_are_administrators = self.updates[0].message.chat.all_members_are_administrators
		self.chat_photo = self.updates[0].message.chat.photo
		self.chat_description = self.updates[0].message.chat.description
		self.chat_invite_link = self.updates[0].message.chat.invite_link
		self.chat_pinned_message = self.updates[0].message.chat.pinned_message
		self.chat_permissions = self.updates[0].message.chat.permissions
		
		# MESSAGE SETTINGS
		self.message_id = self.updates[0].message.message_id
		self.message_date = self.updates[0].message.date
		self.message_text = self.updates[0].message.text
		self.message_caption = self.updates[0].message.caption
		self.message_entities = self.updates[0].message.entities
		self.message_caption_entities = self.updates[0].message.caption_entities
		self.message_audio = self.updates[0].message.audio
		self.message_document = self.updates[0].message.document
		self.message_animation = self.updates[0].message.animation
		self.message_game = self.updates[0].message.game
		self.message_photo = self.updates[0].message.photo
		self.message_sticker = self.updates[0].message.sticker
		self.message_video = self.updates[0].message.video
		self.message_video_note = self.updates[0].message.video_note
		self.message_voice = self.updates[0].message.voice
		self.message_contact = self.updates[0].message.contact
		self.message_dice = self.updates[0].message.dice
		self.message_location = self.updates[0].message.location
		self.message_venue = self.updates[0].message.venue
		
		# ACTIONS
		self.message_new_chat_members = self.updates[0].message.new_chat_members
		self.message_left_chat_member = self.updates[0].message.left_chat_member
		self.message_new_chat_title = self.updates[0].message.new_chat_title
		self.message_new_chat_photo = self.updates[0].message.new_chat_photo
		self.message_delete_chat_photo = self.updates[0].message.delete_chat_photo
		self.message_group_chat_created = self.updates[0].message.group_chat_created
		self.message_supergroup_chat_created = self.updates[0].message.supergroup_chat_created
		self.message_channel_chat_created = self.updates[0].message.channel_chat_created
		self.message_migrate_to_chat_id = self.updates[0].message.migrate_to_chat_id
		self.message_migrate_from_chat_id = self.updates[0].message.migrate_from_chat_id
		self.message_pinned_message = self.updates[0].message.pinned_message
		self.message_successful_payment = self.updates[0].message.successful_payment
		self.message_connected_website = self.updates[0].message.connected_website
		self.message_proximity_alert_triggered = self.updates[0].message.proximity_alert_triggered
		self.message_voice_chat_scheduled = self.updates[0].message.voice_chat_scheduled
		self.message_voice_chat_started = self.updates[0].message.voice_chat_started
		self.message_voice_chat_ended = self.updates[0].message.voice_chat_ended
		self.message_voice_chat_participants_invited = self.updates[0].message.voice_chat_participants_invited
		self.message_reply_to_message = self.updates[0].message.reply_to_message
		self.message_via_bot = self.updates[0].message.via_bot
		self.message_edit_date = self.updates[0].message.edit_date
		self.message_media_group_id = self.updates[0].message.media_group_id
		self.message_entities = self.updates[0].message.entities
	
		# GROUP DATA RETRIEVAL
		self.group_data = self.bot.get_chat(self.chat_id)
		self.group_id = self.group_data.id
		self.group_type = self.group_data.type
		
		# GROUP SETTINGS
		self.group_title = self.group_data.title
		self.group_username = self.group_data.username
		self.group_first_name = self.group_data.first_name
		self.group_last_name = self.group_data.last_name
		self.group_all_members_are_administrators = self.group_data.all_members_are_administrators
		self.group_photo = self.group_data.photo
		self.group_description = self.group_data.description
		self.group_invite_link = self.group_data.invite_link
		self.group_pinned_message = self.group_data.pinned_message
		self.group_permissions = self.group_data.permissions
		self.group_slow_mode_delay = self.group_data.slow_mode_delay
		self.group_sticker_set_name = self.group_data.sticker_set_name
		self.group_can_set_sticker_set = self.group_data.can_set_sticker_set
		self.group_linked_chat_id = self.group_data.linked_chat_id
		self.group_location = self.group_data.location
		self.group_message_auto_delete_time = self.group_data.message_auto_delete_time
		self.group_default_auto_archive_time = self.group_data.default_auto_archive_time
		self.group_unread_count = self.group_data.unread_count
		self.group_last_read_inbox_message_id = self.group_data.last_read_inbox_message_id
		self.group_last_read_outbox_message_id = self.group_data.last_read_outbox_message_id
		self.group_unread_mention_count = self.group_data.unread_mention_count
		self.group_notification_settings = self.group_data.notification_settings
		self.group_reply_markup = self.group_data.reply_markup
		self.group_bot = self.group_data.bot
		self.group_can_join_groups = self.group_data.can_join_groups
		self.group_can_read_all_group_messages = self.group_data.can_read_all_group_messages
		self.group_supports_inline_queries = self.group_data.supports_inline_queries
		self.group_username = self.group_data.username
		self.group_first_name = self.group_data.first_name
		self.group_last_name = self.group_data.last_name
		self.group_photo = self.group_data.photo
		self.group_description = self.group_data.description
		self.group_invite_link = self.group_data.invite_link
		self.group_pinned_message = self.group_data.pinned_message
		self.group_permissions = self.group_data.permissions
		self.group_slow_mode_delay = self.group_data.slow_mode_delay
		self.group_sticker_set_name = self.group_data.sticker_set_name
		self.group_can_set_sticker_set = self.group_data.can_set_sticker_set
		self.group_linked_chat_id = self.group_data.linked_chat_id
		self.group_location = self.group_data.location
		self.group_message_auto_delete_time = self.group_data.message_auto_delete_time
		self.group_default_auto_archive_time = self.group_data.default_auto_archive_time
		self.group_unread_count = self.group_data.unread_count
		self.group_last_read_inbox_message_id = self.group_data.last_read_inbox_message_id
		self.group_last_read_outbox_message_id = self.group_data.last_read_outbox_message_id
		
		# GROUP ADMINISTRATORS
		self.group_administrators = self.bot.get_chat_administrators(self.chat_id)
		self.group_administrators_list = []
		for admin in self.group_administrators:
			self.group_administrators_list.append(admin.user.id)
			
		# GROUP MEMBERS
		self.group_members = self.bot.get_chat_members_count(self.chat_id)
		
		# GROUP MEMBER DATA RETRIEVAL
		self.group_member_data = self.bot.get_chat_member(self.chat_id, self.user_id)
		self.group_member_status = self.group_member_data.status
		self.group_member_is_member = self.group_member_data.is_member
		self.group_member_can_be_edited = self.group_member_data.can_be_edited
		self.group_member_can_change_info = self.group_member_data.can_change_info
		self.group_member_can_post_messages = self.group_member_data.can_post_messages
		self.group_member_can_edit_messages = self.group_member_data.can_edit_messages
		self.group_member_can_delete_messages = self.group_member_data.can_delete_messages
		self.group_member_can_invite_users = self.group_member_data.can_invite_users
		self.group_member_can_restrict_members = self.group_member_data.can_restrict_members
		self.group_member_can_pin_messages = self.group_member_data.can_pin_messages
		self.group_member_can_promote_members = self.group_member_data.can_promote_members
		self.group_member_can_send_messages = self.group_member_data.can_send_messages
		self.group_member_can_send_media_messages = self.group_member_data.can_send_media_messages
		self.group_member_can_send_polls = self.group_member_data.can_send_polls
		
		# GROUP MEMBER USER DATA RETRIEVAL
		self.group_member_user_data = self.group_member_data.user
		self.group_member_user_id = self.group_member_user_data.id
		self.group_member_user_is_bot = self.group_member_user_data.is_bot
		self.group_member_user_first_name = self.group_member_user_data.first_name
		self.group_member_user_last_name = self.group_member_user_data.last_name
		self.group_member_user_username = self.group_member_user_data.username
		self.group_member_user_language_code = self.group_member_user_data.language_code
		self.group_member_user_can_join_groups = self.group_member_user_data.can_join_groups
		self.group_member_user_can_read_all_group_messages = self.group_member_user_data.can_read_all_group_messages
		self.group_member_user_supports_inline_queries = self.group_member_user_data.supports_inline_queries
		
		# GROUP MEMBER USER PROFILE PHOTOS
		self.group_member_user_profile_photos = self.bot.get_user_profile_photos(self.group_member_user_id)
		self.group_member_user_profile_photos_total_count = self.group_member_user_profile_photos.total_count
		self.group_member_user_profile_photos_photos = self.group_member_user_profile_photos.photos
		
		# GROUP MEMBER USER PHOTO
		self.group_member_user_photo = self.group_member_user_data.photo
		self.group_member_user_photo_small_file_id = self.group_member_user_photo.small_file_id
		self.group_member_user_photo_small_file_unique_id = self.group_member_user_photo.small_file_unique_id
		self.group_member_user_photo_big_file_id = self.group_member_user_photo.big_file_id
		self.group_member_user_photo_big_file_unique_id = self.group_member_user_photo.big_file_unique_id
		
	def bot_who_knows_everything_and_controls_everything_in_group(self):
		"""Checks if the bot is an administrator in the group."""
		if self.bot_id in self.group_administrators_list:
			return True
		else:
			return False
		
	# there is a modular version of iterating through the group member user data in the modular version of this class.
	# and  iterating it to a csv file.

	def group_member_user_data_to_csv(self):
		"""Iterates through the group member user data and writes it to a csv file."""
		with open('group_member_user_data.csv', 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(["user_id", "is_bot", "first_name", "last_name", "username", "language_code", "can_join_groups", "can_read_all_group_messages", "supports_inline_queries"])
			for user in self.group_member_user_data:
				writer.writerow([user.id, user.is_bot, user.first_name, user.last_name, user.username, user.language_code, user.can_join_groups, user.can_read_all_group_messages, user.supports_inline_queries])
		# The csv file is saved in the same directory as the python file. You can change the name of the file and the directory.
		# This data is the most valuable data in the group. It is the data of the group members. It is the data of
		# the users. It is the data of the people who are in the group. It is the data of the people who are using the bot.
		# Mext append the data to the same csv file. Do not overwrite the data. Append the data. If images, provide links to the images.
		# If videos, provide links to the videos. If audio, provide links to the audio. If documents, provide links to
		# the documents. That's it. That's all you need to do. That's all you need to know. That's all you need to learn.
		# Do not put redundant data in the csv file. Do not put redundant data in the csv file. Do not put redundant data in the csv file.
	
	def group_member_user_history_data_to_csv(self):
		"""Iterates through the group member user history data and writes it to a csv file."""
		
		with open('group_member_user_history_data.csv', 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(["user_id", "is_bot", "first_name", "last_name", "username", "language_code", "can_join_groups", "can_read_all_group_messages", "supports_inline_queries"])
			for user in self.group_member_user_history_data:
				writer.writerow([user.id, user.is_bot, user.first_name, user.last_name, user.username, user.language_code, user.can_join_groups, user.can_read_all_group_messages, user.supports_inline_queries])
		# The csv file is saved in the same directory as the python file. You can change the name of the file and the directory.
	
	def group_member_user_profile_photos_to_csv(self):
		"""Iterates through the group member user profile photos and writes it to a csv file."""
		with open('group_member_user_profile_photos.csv', 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(["user_id", "total_count", "photos"])
			for user in self.group_member_user_profile_photos:
				writer.writerow([user.id, user.total_count, user.photos])
		# The csv file is saved in the same directory as the python file. You can change the name of the file and the directory.
	
	def group_member_user_photo_to_csv(self):
		"""Iterates through the group member user photo and writes it to a csv file."""
		with open('group_member_user_photo.csv', 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(["user_id", "small_file_id", "small_file_unique_id", "big_file_id", "big_file_unique_id"])
			for user in self.group_member_user_photo:
				writer.writerow([user.id, user.small_file_id, user.small_file_unique_id, user.big_file_id, user.big_file_unique_id])
		# The csv file is saved in the same directory as the python file. You can change the name of the file and the directory.
	
	def group_member_current_status_to_updating_csv(self):
		"""Writes the group member current status to a csv file."""
		with open('group_member_current_status.csv', 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(["group_member_current_status"])
			writer.writerow([self.group_member_current_status])
		# The csv file is saved in the same directory as the python file. You can change the name of the file and the directory.
	
	def create_group_member_current_status_updating_csv(self):
		"""Creates the group member current status updating csv file."""
		with open('group_member_current_status.csv', 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(["group_member_current_status"])
		# The csv file is saved in the same directory as the python file. You can change the name of the file and the directory.
	
	def append_group_member_current_status_to_updating_csv(self):
		"""Appends the group member current status to the updating csv file."""
		with open('group_member_current_status.csv', 'a', newline='') as file:
			writer = csv.writer(file)
			writer.writerow([self.group_member_current_status])
		# The csv file is saved in the same directory as the python file. You can change the name of the file and the directory.
	
	def group_member_current_status_to_csv(self):
		"""Writes the group member current status to a csv file."""
		with open('group_member_current_status.csv', 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(["group_member_current_status"])
			writer.writerow([self.group_member_current_status])
		# The csv file is saved in the same directory as the python file. You can change the name of the file and the directory.
	
	def create_the_csv(self):
		"""Creates the csv file."""
		self.create_group_member_current_status_updating_csv()
		self.create_group_member_user_history_data_updating_csv()
		self.create_group_member_user_profile_photos_updating_csv()
		self.create_group_member_user_photo_updating_csv()
		
	def append_to_the_csv(self):
		"""Appends to the csv file."""
		self.append_group_member_current_status_to_updating_csv()
		self.append_group_member_user_history_data_to_updating_csv()
		self.append_group_member_user_profile_photos_to_updating_csv()
		self.append_group_member_user_photo_to_updating_csv()
		
	def write_to_the_csv(self):
		"""Writes to the csv file."""
		self.group_member_current_status_to_csv()
		self.group_member_user_history_data_to_csv()
		self.group_member_user_profile_photos_to_csv()
		self.group_member_user_photo_to_csv()
		
	def update_the_csv(self):
		"""Updates the csv file."""
		self.write_to_the_csv()
		self.create_the_csv()
		self.append_to_the_csv()
		
	def get_group_member_current_status(self):
		"""Gets the group member current status."""
		self.group_member_current_status = self.bot.get_chat_member(self.group_id, self.user_id).status
		print(self.group_member_current_status)
		
	def get_group_member_user_history_data(self):
		"""Gets the group member user history data."""
		self.group_member_user_history_data = self.bot.get_chat_member(self.group_id, self.user_id).user
		print(self.group_member_user_history_data)
		
	def get_group_member_user_profile_photos(self):
		"""Gets the group member user profile photos."""
		self.group_member_user_profile_photos = self.bot.get_user_profile_photos(self.user_id)
		print(self.group_member_user_profile_photos)
		
	def get_group_member_user_photo(self):
		"""Gets the group member user photo."""
		self.group_member_user_photo = self.bot.get_user_profile_photos(self.user_id).photos[0]
		print(self.group_member_user_photo)
	
	def get_all_group_member_data(self):
		"""Gets all group member data."""
		self.get_group_member_current_status()
		self.get_group_member_user_history_data()
		self.get_group_member_user_profile_photos()
		self.get_group_member_user_photo()
		
	def update_all_group_member_data(self):
		"""Updates all group member data."""
		self.get_all_group_member_data()
		self.update_the_csv()
		
	def get_all_group_member_data_and_update_the_csv(self):
		"""Gets all group member data and updates the csv file."""
		self.update_all_group_member_data()
		
	def get_all_group_member_data_and_update_the_csv_every_5_seconds(self, seconds):
		"""Gets all group member data and updates the csv file every n seconds."""
		while True:
			self.get_all_group_member_data_and_update_the_csv()
			time.sleep(seconds)
			
			
	# Now create bindings to the telegram library and modules for the above generalized functions.
	# The following functions are for the telegram library. We make a new class for this.

class TelegramLibrary:
	"""Creates bindings to the telegram library."""
	
	def __init__(self):
		"""Initializes the class."""
		self.bot = telegram
		self.updater = Updater
		self.dispatcher = Dispatcher
		self.job_queue = JobQueue
		self.job = Job
		self.message = Message
		self.chat = Chat
		self.user = User
		self.chat_member = ChatMember
		self.chat_member_updated = ChatMemberUpdated
		self.chat_permissions = ChatPermissions
		self.chat_photo = ChatPhoto
		self.file = File
		self.sticker = Sticker
		self.sticker_set = StickerSet
		self.inline_query = InlineQuery
		self.inline_query_result = InlineQueryResult
		
		# use only wha's necessary for the abofe generalized functions. There is a bijection between the telegram library and the generalized functions.
	
	def get_bot(self):
		"""Gets the bot."""
		return self.bot
	
	def get_updater(self):
		"""Gets the updater."""
		return self.updater
	
	def get_dispatcher(self):
		"""Gets the dispatcher."""
		return self.dispatcher
	
	def get_job_queue(self):
		"""Gets the job queue."""
		return self.job_queue
	
	def get_job(self):
		"""Gets the job."""
		return self.job
	
	def get_message(self):
		"""Gets the message."""
		return self.message
	
	def get_chat(self):
		"""Gets the chat."""
		return self.chat
	
	def get_user(self):
		"""Gets the user."""
		return self.user
	
	def get_chat_member(self):
		"""Gets the chat member."""
		return self.chat_member
	
	def get_chat_member_updated(self):
		"""Gets the chat member updated."""
		return self.chat_member_updated
	
	def get_chat_permissions(self):
		"""Gets the chat permissions."""
		return self.chat_permissions
	
	def get_chat_photo(self):
		"""Gets the chat photo."""
		return self.chat_photo
	
	
	# Now create bindings to the telegram modules for the above generalized functions.
	# The following functions are for the telegram modules. We make a new class for this.
	
class TelegramModules:
	"""Creates bindings to the telegram modules."""
	
	def __init__(self):
		"""Initializes the class."""
		self.bot = Bot
		self.updater = Updater
		self.dispatcher = Dispatcher
		self.job_queue = JobQueue
		self.job = Job
		self.message = Message
		self.chat = Chat
		self.user = User
		self.chat_member = ChatMember
		self.chat_member_updated = ChatMemberUpdated
		self.chat_permissions = ChatPermissions
		self.chat_photo = ChatPhoto
		self.file = File
		self.sticker = Sticker
		self.sticker_set = StickerSet
		self.inline_query = InlineQuery
		self.inline_query_result = InlineQueryResult
		
		# use only wha's necessary for the abofe generalized functions. There is a bijection between the telegram modules and the generalized functions.
	
	def get_bot(self):
		"""Gets the bot."""
		return self.bot
	
	def get_updater(self):
		"""Gets the updater."""
		return self.updater
	
	def get_dispatcher(self):
		"""Gets the dispatcher."""
		return self.dispatcher
	
	def get_job_queue(self):
		"""Gets the job queue."""
		return self.job_queue
	
	def get_job(self):
		"""Gets the job."""
		return self.job
	
	def get_message(self):
		"""Gets the message."""
		return self.message
	
	def get_chat(self):
		"""Gets the chat."""
		return self.chat
	
	def get_user(self):
		"""Gets the user."""
		return self.user
	
	def get_chat_member(self):
		"""Gets the chat member."""
		return self.chat_member
	
	def get_chat_member_updated(self):
		"""Gets the chat member updated."""
		return self.chat_member_updated
	
	def get_chat_permissions(self):
		"""Gets the chat permissions."""
		return self.chat_permissions
	
	def get_chat_photo(self):
		"""Gets the chat photo."""
		return self.chat_photo
	
	
	# Now create bindings to the telegram library and modules for the above generalized functions.
	# The following functions are for the telegram library and modules. We make a new class for this.

class TelegramLibraryAndModules:
	"""Creates bindings to the telegram library and modules."""
	
	def __init__(self):
		"""Initializes the class."""
		self.bot = telegram.Bot
		self.updater = telegram.ext.Updater
		self.dispatcher = telegram.ext.Dispatcher
		self.job_queue = telegram.ext.JobQueue
		self.job = telegram.ext.Job
		self.message = telegram.Message
		self.chat = telegram.Chat
		self.user = telegram.User
		self.chat_member = telegram.ChatMember
		self.chat_member_updated = telegram.ChatMemberUpdated
		self.chat_permissions = telegram.ChatPermissions
		self.chat_photo = telegram.ChatPhoto
		self.file = telegram.File
		self.sticker = telegram.Sticker
		self.sticker_set = telegram.StickerSet
		self.inline_query = telegram.InlineQuery
		self.inline_query_result = telegram.InlineQueryResult
		
		# use only wha's necessary for the abofe generalized functions. There is a bijection between the telegram library and modules and the generalized functions.
	
	def get_bot(self):
		"""Gets the bot."""
		return self.bot
	
	def get_updater(self):
		"""Gets the updater."""
		return self.updater
	
	def get_dispatcher(self):
		"""Gets the dispatcher."""
		return self.dispatcher
	
	def get_job_queue(self):
		"""Gets the job queue."""
		return self.job_queue
	
	def get_job(self):
		"""Gets the job."""
		return self.job
	
	def get_message(self):
		"""Gets the message."""
		return self.message
	
	def get_chat(self):
		"""Gets the chat."""
		return self.chat
	
	def get_user(self):
		"""Gets the user."""
		return self.user
	
	def get_chat_member(self):
		"""Gets the chat member."""
		return self.chat_member
	
	def get_chat_member_updated(self):
		"""Gets the chat member updated."""
		return self.chat_member_updated
	
	def get_chat_permissions(self):
		"""Gets the chat permissions."""
		return self.chat_permissions
	
	def get_chat_photo(self):
		"""Gets the chat photo."""
		return self.chat_photo
	
	# Now create bijections between the telegram library and modules and the generalized functions.

class Bijection:
	"""Creates bijections between the telegram library and modules and the generalized functions."""
	
	def __init__(self):
		"""Initializes the class."""
		self.telegram_modules = TelegramModules()
		self.telegram_library_and_modules = TelegramLibraryAndModules()
		
		# use only wha's necessary for the abofe generalized functions. There is a bijection between the telegram library and modules and the generalized functions.
	
	def get_bot(self):
		"""Gets the bot."""
		return self.telegram_modules.get_bot()
	
	def get_updater(self):
		"""Gets the updater."""
		return self.telegram_modules.get_updater()
	
	def get_dispatcher(self):
		"""Gets the dispatcher."""
		return self.telegram_modules.get_dispatcher()
	
	def get_job_queue(self):
		"""Gets the job queue."""
		return self.telegram_modules.get_job_queue()
	
	def get_job(self):
		"""Gets the job."""
		return self.telegram_modules.get_job()
	
	def get_message(self):
		"""Gets the message."""
		return self.telegram_modules.get_message()
	
	def get_chat(self):
		"""Gets the chat."""
		return self.telegram_modules.get_chat()
	
	def get_user(self):
		"""Gets the user."""
		return self.telegram_modules.get_user()
	
	def get_chat_member(self):
		"""Gets the chat member."""
		return self.telegram_modules.get_chat_member()
	
	def get_chat_member_updated(self):
		"""Gets the chat member updated."""
		return self.telegram_modules.get_chat_member_updated()
	
	def get_chat_permissions(self):
		"""Gets the chat permissions."""
		return self.telegram_modules.get_chat_permissions()
	
	def get_chat_photo(self):
		"""Gets the chat photo."""
		return self.telegram_modules.get_chat_photo()
	
	# Now create a master folder for all the data, one huge vcs file, and in a folder possible images, etc. ,
 	# but no need to download them. Just links in the cvs file is enough.

class MasterFolder:
	"""Creates a master folder for all the data, one huge vcs file, and in a folder possible images, etc. , but no need to download them. Just links in the cvs file is enough."""
	
	def __init__(self):
		"""Initializes the class."""
		self.master_folder = "master_folder"
		self.master_file = "master_file.csv"
		self.images_folder = "images"
		self.images_file = "images.csv"
		
		# use only wha's necessary for the abofe generalized functions. There is a bijection between the telegram library and modules and the generalized functions.
	
	def get_master_folder(self):
		"""Gets the master folder."""
		return self.master_folder
	
	def get_master_file(self):
		"""Gets the master file."""
		return self.master_file
	
	def get_images_folder(self):
		"""Gets the images folder."""
		return self.images_folder
	
	def get_images_file(self):
		"""Gets the images file."""
		return self.images_file
	
	# Now create a class for the master file.

class MasterFile:
	"""Creates a class for the master file."""
	
	def __init__(self):
		"""Initializes the class."""
		self.master_file = MasterFolder().get_master_file()
		self.images_file = MasterFolder().get_images_file()
		
		# use only wha's necessary for the abofe generalized functions. There is a bijection between the telegram library and modules and the generalized functions.
	
	def get_master_file(self):
		"""Gets the master file."""
		return self.master_file
	
	def get_images_file(self):
		"""Gets the images file."""
		return self.images_file
	
	# Now create a class for the rest of the data, meaning media: images, videos, etc. One class is enough
	# for all the media, documnents etc.

class Media:
	"""Creates a class for the rest of the data, meaning media: images, videos, etc. One class is enough for all the media, documnents etc."""
	
	def __init__(self):
		"""Initializes the class."""
		self.images_folder = MasterFolder().get_images_folder()
		self.images_file = MasterFile().get_images_file()
		
		# use only wha's necessary for the abofe generalized functions. There is a bijection between the telegram library and modules and the generalized functions.
	
	def get_images_folder(self):
		"""Gets the images folder."""
		return self.images_folder
	
	def get_images_file(self):
		"""Gets the images file."""
		return self.images_file
	
	def get_image(self):
		"""Gets the image."""
		return self.image # the image is a link to the image in the images folder.
	
	# Now create a class for the bot.

class Bot:
	"""Creates a class for the bot."""
	
	def __init__(self):
		"""Initializes the class."""
		self.bot = Bijection().get_bot()
		self.updater = Bijection().get_updater()
		self.dispatcher = Bijection().get_dispatcher()
		self.job_queue = Bijection().get_job_queue()
		self.job = Bijection().get_job()
		self.message = Bijection().get_message()
		self.chat = Bijection().get_chat()
		self.user = Bijection().get_user()
		self.chat_member = Bijection().get_chat_member()
		self.chat_member_updated = Bijection().get_chat_member_updated()
		self.chat_permissions = Bijection().get_chat_permissions()
		self.chat_photo = Bijection().get_chat_photo()
		self.master_folder = MasterFolder().get_master_folder()
		self.master_file = MasterFile().get_master_file()
		self.images_folder = Media().get_images_folder()
		self.images_file = Media().get_images_file()
		
		# use only wha's necessary for the abofe generalized functions. There is a bijection between the telegram library and modules and the generalized functions.
	
	def get_bot(self):
		"""Gets the bot."""
		return self.bot
	
	def get_updater(self):
		"""Gets the updater."""
		return self.updater
	
	def get_dispatcher(self):
		"""Gets the dispatcher."""
		return self.dispatcher
	
	def get_job_queue(self):
		"""Gets the job queue."""
		return self.job_queue
	
	def get_job(self):
		"""Gets the job."""
		return self.job
	
	def get_message(self):
		"""Gets the message."""
		return self.message
	
	def get_chat(self):
		"""Gets the chat."""
		return self.chat
	
	def get_user(self):
		"""Gets the user."""
		return self.user
	
	def get_chat_member(self):
		"""Gets the chat member."""
		return self.chat_member
	
	def get_chat_member_updated(self):
		"""Gets the chat member updated."""
		return self.chat_member_updated
	
	def get_chat_permissions(self):
		"""Gets the chat permissions."""
		return self.chat_permissions
	
	def get_chat_photo(self):
		"""Gets the chat photo."""
		return self.chat_photo
	
	def get_master_folder(self):
		"""Gets the master folder."""
		return self.master_folder
	
	def get_master_file(self):
		"""Gets the master file."""
		return
	
	
	# Now create a class for the bot's commands.

class BotWorkerCommands:
	"""
	This bot is only for data retrieval. It does not do anything else. It is a bot that works for the bot's commands.
	"""
	
	def __init__(self):
		"""Initializes the class."""
		self.bot = Bot().get_bot()
		self.updater = Bot().get_updater()
		self.dispatcher = Bot().get_dispatcher()
		self.job_queue = Bot().get_job_queue()
		self.job = Bot().get_job()
		self.message = Bot().get_message()
		self.chat = Bot().get_chat()
		self.user = Bot().get_user()
		self.chat_member = Bot().get_chat_member()
		self.chat_member_updated = Bot().get_chat_member_updated()
		self.chat_permissions = Bot().get_chat_permissions()
		self.chat_photo = Bot().get_chat_photo()
		self.master_folder = Bot().get_master_folder()
		self.master_file = Bot().get_master_file()
		self.images_folder = Bot().get_images_folder()
		self.images_file = Bot().get_images_file()
		
		# use only wha's necessary for the abofe generalized functions. There is a bijection between the telegram library and modules and the generalized functions.
	
	def get_bot(self):
		"""Gets the bot."""
		return self.bot
	
	def get_updater(self):
		"""Gets the updater."""
		return self.updater
	
	def get_dispatcher(self):
		"""Gets the dispatcher."""
		return self.dispatcher
	
	def get_job_queue(self):
		"""Gets the job queue."""
		return self.job_queue
	
	def get_job(self):
		"""Gets the job."""
		return self.job
	
	def get_message(self):
		"""Gets the message."""
		return self.message
	
	def get_chat(self):
		"""Gets the chat."""
		return self.chat
	
	def get_user(self):
		"""Gets the user."""
		return self.user
	
	def get_chat_member(self):
		"""Gets the chat member."""
		return self.chat_member
	
	def get_chat_member_updated(self):
		"""Gets the chat member updated."""
		return self.chat_member_updated
	
	def get_chat_permissions(self):
		"""Gets the chat permissions."""
		return self.chat_permissions
	
	def get_chat_photo(self):
		"""Gets the chat photo."""
		return self.chat_photo
	
	def get_master_folder(self):
		"""Gets the master folder."""
		return self.master_folder
	
	def get_master_file(self):
		"""Gets the master file."""
		return self.master_file
	
	def get_images_folder(self):
		"""Gets the images folder."""
		return self.images_folder
	
	def get_images_file(self):
		"""Gets the images file."""
		return self.images_file
	
	def start(self, bot, update):
		"""Starts the bot."""
		bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
		
	def help(self, bot, update):
		"""Helps the user."""
		bot.send_message(chat_id=update.message.chat_id, text="Help!")
		
	def echo(self, bot, update):
		"""Echoes the user."""
		bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
		
	def error(self, bot, update, error):
		"""Logs errors."""
		logger.warning('Update "%s" caused error "%s"', update, error)
		
	def unknown(self, bot, update):
		"""Logs unknown commands."""
		bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
		
	def main(self):
		"""Starts the bot."""
		self.updater.start_polling()
		self.updater.idle()
		
	def run(self):
		"""Runs the bot."""
		self.dispatcher.add_handler(CommandHandler("start", self.start))
		self.dispatcher.add_handler(CommandHandler("help", self.help))
		self.dispatcher.add_handler(MessageHandler(Filters.text, self.echo))
		self.dispatcher.add_error_handler(self.error)
		self.dispatcher.add_handler(MessageHandler(Filters.command, self.unknown))
		self.main()
		
	def __del__(self):
		"""Deletes the class."""
		pass
	
	# Now create a class for the bot's jobs.

class BotWorkerJobs:
	
	def __init__(self):
		"""Initializes the class."""
		self.bot = Bot().get_bot()
		self.updater = Bot().get_updater()
		self.dispatcher = Bot().get_dispatcher()
		self.job_queue = Bot().get_job_queue()
		self.job = Bot().get_job()
		self.message = Bot().get_message()
		self.chat = Bot().get_chat()
		self.user = Bot().get_user()
		self.chat_member = Bot().get_chat_member()
		self.chat_member_updated = Bot().get_chat_member_updated()
		self.chat_permissions = Bot().get_chat_permissions()
		self.chat_photo = Bot().get_chat_photo()
		self.master_folder = Bot().get_master_folder()
		self.master_file = Bot().get_master_file()
		self.images_folder = Bot().get_images_folder()
		self.images_file = Bot().get_images_file()
		
		# use only wha's necessary for the abofe generalized functions. There is a bijection between the telegram library and modules and the generalized functions.
	
	def get_bot(self):
		"""Gets the bot."""
		return self.bot
	
	def get_updater(self):
		"""Gets the updater."""
		return self.updater
	
	def get_dispatcher(self):
		"""Gets the dispatcher."""
		return self.dispatcher
	
	def get_job_queue(self):
		"""Gets the job queue."""
		return self.job_queue
	
	def get_job(self):
		"""Gets the job."""
		return self.job
	
	def get_message(self):
		"""Gets the message."""
		return self.message
	
	def get_chat(self):
		"""Gets the chat."""
		return self.chat
	
	def get_user(self):
		"""Gets the user."""
		return self.user
	
	def get_chat_member(self):
		"""Gets the chat member."""
		return self.chat_member
	
	def get_chat_member_updated(self):
		"""Gets the chat member updated."""
		return self.chat_member_updated
	
	def get_chat_permissions(self):
		"""Gets the chat permissions."""
		return self.chat_permissions
	
	def get_chat_photo(self):
		"""Gets the chat photo."""
		return self.chat_photo
	
	def get_master_folder(self):
		"""Gets the master folder."""
		return self.master_folder
	
	def get_master_file(self):
		"""Gets the master file."""
		return self.master_file
	
	def get_images_folder(self):
		"""Gets the images folder."""
		return self.images_folder
	
	def get_images_file(self):
		"""Gets the images file."""
		return self.images_file
	
	def job_index(self, bot, job, index):
		bot.send_message(chat_id=job.context, text=f'Job {index}!')

	
	def run(self):
		"""Runs the bot."""
		self.job_queue.run_repeating(self.job_index, interval=5, first=0, context=1)
		
	def __del__(self):
		"""Deletes the class."""
		pass
	
	# Now create a class for the bot's commands.

class BotWorkerCommands:
	
	def __init__(self):
		"""Initializes the class."""
		self.bot = Bot().get_bot()
		self.updater = Bot().get_updater()
		self.dispatcher = Bot().get_dispatcher()
		self.job_queue = Bot().get_job_queue()
		self.job = Bot().get_job()
		self.message = Bot().get_message()
		self.chat = Bot().get_chat()
		self.user = Bot().get_user()
		self.chat_member = Bot().get_chat_member()
		self.chat_member_updated = Bot().get_chat_member_updated()
		self.chat_permissions = Bot().get_chat_permissions()
		self.chat_photo = Bot().get_chat_photo()
		self.master_folder = Bot().get_master_folder()
		self.master_file = Bot().get_master_file()
		self.images_folder = Bot().get_images_folder()
		self.images_file = Bot().get_images_file()
		
		# use only wha's necessary for the abofe generalized functions. There is a bijection between the telegram library and modules and the generalized functions.
		# how are these different to above one?
	def get_bot(self):
		"""Gets the bot."""
		return self.bot
	
	def get_updater(self):
		"""Gets the updater."""
		return self.updater
	
	def get_dispatcher(self):
		"""Gets the dispatcher."""
		return self.dispatcher
	
	def get_job_queue(self):
		"""Gets the job queue."""
		return self.job_queue
	
	def get_job(self):
		"""Gets the job."""
		return self.job
	
	def get_message(self):
		"""Gets the message."""
		return self.message
	
	def get_chat(self):
		"""Gets the chat."""
		return self.chat
	
	def get_user(self):
		"""Gets the user."""
		return self.user
	
	def get_chat_member(self):
		"""Gets the chat member."""
		return self.chat_member
	
	def get_chat_member_updated(self):
		"""Gets the chat member updated."""
		return self.chat_member_updated
	
	def get_chat_permissions(self):
		"""Gets the chat permissions."""
		return self.chat_permissions
	
	def get_chat_photo(self):
		"""Gets the chat photo."""
		return self.chat_photo
	
	def get_master_folder(self):
		"""Gets the master folder."""
		return self.master_folder
	
	def get_master_file(self):
		"""Gets the master file."""
		return self.master_file
	
	def get_images_folder(self):
		"""Gets the images folder."""
		return self.images_folder

	def get_images_file(self):
		"""Gets the images file."""
		return self.images_file
	
	def start(self, bot, update):
		"""Starts the bot."""
		bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
		
	def help(self, bot, update):
		"""Helps the user."""
		bot.send_message(chat_id=update.message.chat_id, text="Help!")
		
	def echo(self, bot, update):
		"""Echos the user."""
		bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
		
	def error(self, bot, update, error):
		"""Logs errors."""
		logger.warning('Update "%s" caused error "%s"', update, error)
		
	def __del__(self):
		"""Deletes the class."""
		pass
	
	# Now create a class for the bot's handlers.

class BotWorkerHandlers:
	
	def __init__(self):
		"""Initializes the class."""
		self.bot = Bot().get_bot()
		self.updater = Bot().get_updater()
		self.dispatcher = Bot().get_dispatcher()
		self.job_queue = Bot().get_job_queue()
		self.job = Bot().get_job()
		self.message = Bot().get_message()
		self.chat = Bot().get_chat()
		self.user = Bot().get_user()
		self.chat_member = Bot().get_chat_member()
		self.chat_member_updated = Bot().get_chat_member_updated()
		self.chat_permissions = Bot().get_chat_permissions()
		self.chat_photo = Bot().get_chat_photo()
		self.master_folder = Bot().get_master_folder()
		self.master_file = Bot().get_master_file()
		self.images_folder = Bot().get_images_folder()
		self.images_file = Bot().get_images_file()
		
		# use only wha's necessary for the abofe generalized functions. There is a bijection between the telegram library and modules and the generalized functions.
		# how are these different to above one?
	def get_bot(self):
		"""Gets the bot."""
		return self.bot
	
	def get_updater(self):
		"""Gets the updater."""
		return self.updater
	
	def get_dispatcher(self):
		"""Gets the dispatcher."""
		return self.dispatcher
	
	def get_job_queue(self):
		"""Gets the job queue."""
		return self.job_queue
	
	def get_job(self):
		"""Gets the job."""
		return self.job
	
	def get_message(self):
		"""Gets the message."""
		return self.message
	
	def get_chat(self):
		"""Gets the chat."""
		return self.chat
	
	def get_user(self):
		"""Gets the user."""
		return self.user
	
	def get_chat_member(self):
		"""Gets the chat member."""
		return self.chat_member
	
	def get_chat_member_updated(self):
		"""Gets the chat member updated."""
		return self.chat_member_updated
	
	def get_chat_permissions(self):
		"""Gets the chat permissions."""
		return self.chat_permissions
	
	def get_chat_photo(self):
		"""Gets the chat photo."""
		return self.chat_photo
	
	def get_master_folder(self):
		"""Gets the master folder."""
		return self.master_folder
	
	def get_master_file(self):
		"""Gets the master file."""
		return self.master_file
	
	def get_images_folder(self):
		"""Gets the images folder."""
		return self.images_folder
	
	def get_images_file(self):
		"""Gets the images file."""
		return self.images_file
	
	def start(self, bot, update):
		"""Starts the bot."""
		Bot().start(bot, update)
		
	def help(self, bot, update):
		"""Helps the user."""
		Bot().help(bot, update)
		
	def echo(self, bot, update):
		"""Echos the user."""
		Bot().echo(bot, update)
		
	def error(self, bot, update, error):
		"""Logs errors."""
		Bot().error(bot, update, error)
		
	def __del__(self):
		"""Deletes the class."""
		pass
	
	# Now create a class for the bot's handlers. # didn you do it already?
# We need to make one more bot class: JobBrokerBot, which is a subclass of Bot. This class will be used to create a
# bot that will be used to schedule jobs. And comprise all the functions that are necessary for the job broker bot.
class BotWorker:
	
	def __init__(self):
		"""Initializes the class."""
		self.bot = Bot().get_bot()
		self.updater = Bot().get_updater()
		self.dispatcher = Bot().get_dispatcher()
		self.job_queue = Bot().get_job_queue()
		self.job = Bot().get_job()
		self.message = Bot().get_message()
		self.chat = Bot().get_chat()
		self.user = Bot().get_user()
		self.chat_member = Bot().get_chat_member()
		self.chat_member_updated = Bot().get_chat_member_updated()
		self.chat_permissions = Bot().get_chat_permissions()
		self.chat_photo = Bot().get_chat_photo()
		self.master_folder = Bot().get_master_folder()
		self.master_file = Bot().get_master_file()
		self.images_folder = Bot().get_images_folder()
		self.images_file = Bot().get_images_file()
		
		# use only wha's necessary for the abofe generalized functions. There is a bijection between the telegram library and modules and the generalized functions.
		# how are these different to above one?
	def get_bot(self):
		"""Gets the bot."""
		return self.bot
	
	def get_updater(self):
		"""Gets the updater."""
		return self.updater
	
	def get_dispatcher(self):
		"""Gets the dispatcher."""
		return self.dispatcher
	
	def get_job_queue(self):
		"""Gets the job queue."""
		return self.job_queue
	
	def get_job(self):
		"""Gets the job."""
		return self.job
	
	def get_message(self):
		"""Gets the message."""
		return self.message
	
	def get_chat(self):
		"""Gets the chat."""
		return self.chat
	
	def get_user(self):
		"""Gets the user."""
		return self.user
	
	def get_chat_member(self):
		"""Gets the chat member."""
		return self.chat_member
	
	def get_chat_member_updated(self):
		"""Gets the chat member updated."""
		return self.chat_member_updated
	
	def get_chat_permissions(self):
		"""Gets the chat permissions."""
		return self.chat_permissions
	
	def get_chat_photo(self):
		"""Gets the chat photo."""
		return self.chat_photo
	
	def get_master_folder(self):
		"""Gets the master folder."""
		return self.master_folder
	
	def get_master_file(self):
		"""Gets the master file."""
		return self.master_file
	
	def get_images_folder(self):
		"""Gets the images folder."""
		return self.images_folder
	
	def get_images_file(self):
		"""Gets the images file."""
		return self.images_file
	
	def start(self, bot, update):
		"""Starts the bot."""
		Bot().start(bot, update)
		
	def help(self, bot, update):
		"""Helps the user."""
		Bot().help(bot, update)
		
	def echo(self, bot, update):
		"""Echos the user."""
		Bot().echo(bot, update)
		
	def error(self, bot, update, error):
		"""Logs errors."""
		Bot().error(bot, update, error)
		
	def __del__(self):
		"""Deletes the class."""
		pass
	
	# Now create a class for the bot's handlers. # didn you do it already?
class BotHandlers:
	
	def __init__(self):
		"""Initializes the class."""
		self.bot = Bot().get_bot()
		self.updater = Bot().get_updater()
		self.dispatcher = Bot().get_dispatcher()
		self.job_queue = Bot().get_job_queue()
		self.job = Bot().get_job()
		self.message = Bot().get_message()
		self.chat = Bot().get_chat()
		self.user = Bot().get_user()
		self.chat_member = Bot().get_chat_member()
		self.chat_member_updated = Bot().get_chat_member_updated()
		self.chat_permissions = Bot().get_chat_permissions()
		self.chat_photo = Bot().get_chat_photo()
		self.master_folder = Bot().get_master_folder()
		self.master_file = Bot().get_master_file()
		self.images_folder = Bot().get_images_folder()
		self.images_file = Bot().get_images_file()
		
		# use only wha's necessary for the abofe generalized functions. There is a bijection between the telegram library and modules and the generalized functions.
		# how are these different to above one?
	def get_bot(self):
		"""Gets the bot."""
		return self.bot
	
	def get_updater(self):
		"""Gets the updater."""
		return self.updater
	
	def get_dispatcher(self):
		"""Gets the dispatcher."""
		return self.dispatcher
	
	def get_job_queue(self):
		"""Gets the job queue."""
		return self.job_queue
	
	def get_job(self):
		"""Gets the job."""
		return self.job
	
	def get_message(self):
		"""Gets the message."""
		return self.message
	
	def get_chat(self):
		"""Gets the chat."""
		return self.chat
	
	def get_user(self):
		"""Gets the user."""
		return self.user
	
	def get_chat_member(self):
		"""Gets the chat member."""
		return self.chat_member
	
	def get_chat_member_updated(self):
		"""Gets the chat member updated."""
		return self.chat_member_updated
	
	def get_chat_permissions(self):
		"""Gets the chat permissions."""
		return self.chat_permissions
	
	def get_chat_photo(self):
		"""Gets the chat photo."""
		return self.chat_photo
	
	def get_master_folder(self):
		"""Gets the master folder."""
		return self.master_folder
	
	def get_master_file(self):
		"""Gets the master file."""
		return self.master_file
	
	def get_images_folder(self):
		"""Gets the images folder."""
		return self.images_folder
	
	def get_images_file(self):
		"""Gets the images file."""
		return self.images_file
	
	def start(self, bot, update):
		"""Starts the bot."""
		Bot().start(bot, update)
		
	def help(self, bot, update):
		"""Helps the user."""
		Bot().help(bot, update)
		
	def echo(self, bot, update):
		"""Echos the user."""
		Bot().echo(bot, update)
		
	def error(self, bot, update, error):
		"""Logs errors."""
		Bot().error(bot, update, error)
		
	def __del__(self):
		"""Deletes the class."""
		pass
	
	
	
	
class MasterClassBijectionBot:

def __init__(self):
		"""Initializes the class."""
		self.bot = Bot().get_bot()
		self.updater = Bot().get_updater()
		self.dispatcher = Bot().get_dispatcher()
		self.job_queue = Bot().get_job_queue()
		self.job = Bot().get_job()
		self.message = Bot().get_message()
		self.chat = Bot().get_chat()
		self.user = Bot().get_user()
		self.chat_member = Bot().get_chat_member()
		self.chat_member_updated = Bot().get_chat_member_updated()
		self.chat_permissions = Bot().get_chat_permissions()
		self.chat_photo = Bot().get_chat_photo()
		self.master_folder = Bot().get_master_folder()
		self.master_file = Bot().get_master_file()
		self.images_folder = Bot().get_images_folder()
		self.images_file = Bot().get_images_file()
		
		# use only wha's necessary for the abofe generalized functions. There is a bijection between the telegram library and modules and the generalized functions.
		# how are these different to above one?
	def get_bot(self):
		"""Gets the bot."""
		return self.bot
	
	def get_updater(self):
		"""Gets the updater."""
		return self.updater
	
	def get_dispatcher(self):
		"""Gets the dispatcher."""
		return self.dispatcher
	
	def get_job_queue(self):
		"""Gets the job queue."""
		return self.job_queue
	
	def get_job(self):
		"""Gets the job."""
		return self.job
	
	def get_message(self):
		"""Gets the message."""
		return self.message
	
	def get_chat(self):
		"""Gets the chat."""
		return self.chat
	
	def get_user(self):
		"""Gets the user."""
		return self.user
	
	def get_chat_member(self):
		"""Gets the chat member."""
		return self.chat_member
	
	def get_chat_member_updated(self):
		"""Gets the chat member updated."""
		return self.chat_member_updated
	
	def get_chat_permissions(self):
		"""Gets the chat permissions."""
		return self.chat_permissions
	
	def get_chat_photo(self):
		"""Gets the chat photo."""
		return self.chat_photo
	
	def get_master_folder(self):
		"""Gets the master folder."""
		return self.master_folder
	
	def get_master_file(self):
		"""Gets the master file."""
		return self.master_file
	
	def get_images_folder(self):
		"""Gets the images folder."""
		return self.images_folder
	
	def get_images_file(self):
		"""Gets the images file."""
		return self.images_file
	
	def start(self, bot, update):
		"""Starts the bot."""
		Bot().start(bot, update)
		
	def help(self, bot, update):
		"""Helps the user."""
		Bot().help(bot, update)
		
# tHIS IS NOT GOING ANYWHERE. rEPEATING THE SAME CODE IS NOT GOING TO HELP. How can I help you?
# I am not repeating the same code. I am trying to generalize the functions. I am trying to make a bijection between the telegram library and modules and the generalized functions.
# How are you doing the bijection? What is the bijection? Mapping between one-to-one, as in a csv file,
# there is only one cell to be filled. Even tho we are dealing group information, but it is still discreet enough.
# I am not sure what you mean by bijection. I am trying to make a mapping between the telegram library and modules
# and the generalized functions. Should I use a dictionary? Yes. It is easy to use. But we want to separate the
# individual functions from the generalized functions. No, we are only interested in the data-gathered end product: a
# csv   file. We are not interested in the individual functions. We are interested in the data-gathered end product:
# a csv file and a folders.

# I am not sure what you mean by bijection. I am trying to make a mapping between the telegram library and modules.
# But you don't have to copy the modules here. You can just merge two dictionarys. Iy is the fastest way. Just gather
# the most relevant information listed here, use them as keys, and use a dictionary to map them to the values. Then use
# the dictionary to guide a worker bot to fill in the csv file. Bot uses direct commands to fill the data. It is the
# fastest way. I am not sure what you mean by bijection: I mean the bot is the bijector. It is the bijection between
# the telegram library and modules and the generalized functions. The bot is the bijector.

# You can make a dictionary of telegram librarys attributes in relation to our wanted data. Then use the dictionary to
# guide the bot to fill in the csv file. The bot is the bijector. And then the work is done! The bot is the bijector.

# I am not sure what you mean by bijection. I am trying to make a mapping between the telegram library and modules.
# Well, it is not purely bijection, but I tried to make it overly simple. I am not sure what you mean by bijection.

# Here is a definition of a bijection. You can decide if my analogy was more or less correct. Read carefully below!"
# ------------------------------------------------
# In mathematics, a bijection, also known as a bijective function, one-to-one correspondence, or invertible function, is a function between the elements of two sets, where each element of one set is paired with exactly one element of the other set, and each element of the other set is paired with exactly one element of the first set. There are no unpaired elements. In mathematical terms, a bijective function f: X → Y is a one-to-one (injective) and onto (surjective) mapping of a set X to a set Y.[1] The term one-to-one correspondence must not be confused with one-to-one function (an injective function; see figures).
# A bijection from the set X to the set Y has an inverse function from Y to X. If X and Y are finite sets, then the existence of a bijection means they have the same number of elements. For infinite sets, the picture is more complicated, leading to the concept of cardinal number—a way to distinguish the various sizes of infinite sets.
# A bijective function from a set to itself is also called a permutation, and the set of all permutations of a set forms the symmetric group.
# Bijective functions are essential to many areas of mathematics including the definitions of isomorphism, homeomorphism, diffeomorphism, permutation group, and projective map.
# ------------------------------------------------
# I am not sure what you mean by bijection. I am trying to make a mapping between the telegram library and modules.

#
# Forget bijection. Lets do some real work. Forget biection. Lets do some real work. Forget biection. Lets do some real work.

# If I say, I want the personal data (not media), to a csv file. How would you do it? I would use a dictionary to map
# the telegram library attributes to the csv file attributes. Then I would use the dictionary to guide the bot to fill
# Now its time to make the final connection.


class TelegramDataCrawlerBot:
	
	def __init__(self):
		"""Initializes the bot."""
		self.updater = Updater(token = 'TOKEN')
		self.dispatcher = self.updater.dispatcher
		self.dispatcher.add_handler(CommandHandler('start', self.start))
		self.dispatcher.add_handler(CommandHandler('help', self.help))
		self.dispatcher.add_handler(CommandHandler('get_personal_data', self.get_personal_data))
		self.dispatcher.add_handler(CommandHandler('get_group_data', self.get_group_data))
		self.dispatcher.add_handler(CommandHandler('get_group_members', self.get_group_members))
		self.dispatcher.add_handler(CommandHandler('get_group_member', self.get_group_member))
		self.dispatcher.add_handler(CommandHandler('get_group_member_updated', self.get_group_member_updated))
		self.dispatcher.add_handler(CommandHandler('get_group_member_deleted', self.get_group_member_deleted))
		self.dispatcher.add_handler(CommandHandler('get_group_member_added', self.get_group_member_added))
		self.dispatcher.add_handler(CommandHandler('get_group_member_left', self.get_group_member_left))
		self.dispatcher.add_handler(CommandHandler('get_group_member_kicked', self.get_group_member_kicked))
		self.dispatcher.add_handler(CommandHandler('get_group_member_banned', self.get_group_member_banned))
		self.dispatcher.add_handler(CommandHandler('get_group_member_unbanned', self.get_group_member_unbanned))
		self.dispatcher.add_handler(CommandHandler('get_group_member_restricted', self.get_group_member_restricted))
		self.dispatcher.add_handler(CommandHandler('get_group_member_unrestricted', self.get_group_member_unrestricted))
		self.dispatcher.add_handler(CommandHandler('get_group_member_invited', self.get_group_member_invited))
		self.dispatcher.add_handler(CommandHandler('get_group_member_promoted', self.get_group_member_promoted))
		self.dispatcher.add_handler(CommandHandler('get_group_member_demoted', self.get_group_member_demoted))
		
	def start(self, bot, update):
		"""Sends a message when the command /start is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Hi!')
		
	def help(self, bot, update):
		"""Sends a message when the command /help is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Help!')
		
	def get_personal_data(self, bot, update):
		"""Sends a message when the command /get_personal_data is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Personal data!')
		
	def get_group_data(self, bot, update):
		"""Sends a message when the command /get_group_data is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Group data!')
		
	def get_group_members(self, bot, update):
		"""Sends a message when the command /get_group_members is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Group members!')
		
	def get_group_member(self, bot, update):
		"""Sends a message when the command /get_group_member is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Group member!')
		
	def get_group_member_updated(self, bot, update):
		"""Sends a message when the command /get_group_member_updated is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Group member updated!')
		
	def get_group_member_deleted(self, bot, update):
		"""Sends a message when the command /get_group_member_deleted is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Group member deleted!')
		
	def get_group_member_added(self, bot, update):
		"""Sends a message when the command /get_group_member_added is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Group member added!')
		
	def get_group_member_left(self, bot, update):
		"""Sends a message when the command /get_group_member_left is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Group member left!')
		
	def get_group_member_kicked(self, bot, update):
		"""Sends a message when the command /get_group_member_kicked is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Group member kicked!')
		
	def get_group_member_banned(self, bot, update):
		"""Sends a message when the command /get_group_member_banned is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Group member banned!')
		
	def get_group_member_unbanned(self, bot, update):
		"""Sends a message when the command /get_group_member_unbanned is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Group member unbanned!')
		
	def get_group_member_restricted(self, bot, update):
		"""Sends a message when the command /get_group_member_restricted is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Group member restricted!')
		
	def get_group_member_unrestricted(self, bot, update):
		"""Sends a message when the command /get_group_member_unrestricted is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Group member unrestricted!')
		
	def get_group_member_invited(self, bot, update):
		"""Sends a message when the command /get_group_member_invited is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Group member invited!')
		
	def get_group_member_promoted(self, bot, update):
		"""Sends a message when the command /get_group_member_promoted is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Group member promoted!')
		
	def get_group_member_demoted(self, bot, update):
		"""Sends a message when the command /get_group_member_demoted is issued."""
		bot.send_message(chat_id = update.message.chat_id, text = 'Group member demoted!')
		
	def error(self, bot, update, error):
		"""Log Errors caused by Updates."""
		logger.warning('Update "%s" caused error "%s"', update, error)
		
	def run(self):
		"""Start the bot."""
		# Start the Bot
		self.updater.start_polling()
		
		# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
		# SIGTERM or SIGABRT. This should be used most of the time, since
		# start_polling() is non-blocking and will stop the bot gracefully.
		self.updater.idle()
		
	def autonomous_gathering(self):
		"""Start the autonomous gathering process."""
		pass
	
	def autonomous_processing(self):
		"""Start the autonomous processing process."""
		pass
	
	def autonomous_sending(self):
		"""Start the autonomous sending process."""
		pass # WHy is this here? It's not used anywhere. It's not even called anywhere. But if you need to command it,
		# you can do it from the command line. Just type "python3 bot.py autonomous_sending" and it will run.
		# But it's not used anywhere. So why is it here? Where is the original command? Why is it not here?
	
	def autonomous_sending(self):
		"""Start the autonomous sending process."""
		pass
	
	
if __name__ == '__main__':
	bot = Bot()
	bot.run()  # where is the function? It's not here. It's not even called anywhere. But if you need to command it,
	# you can do it from the command line. Just type "python3 bot.py run" and it will run. Nope. It's not here.
	
	#bot.autonomous_gathering()
	#bot.autonomous_processing()
	#bot.autonomous_sending()
	#bot.autonomous_sending()
	
	bot.run() # None of these does anything. They are not called anywhere. They are not even defined anywhere. We need
	# to define them. We need to call them. We need to do something with them. We need to do something with them.
	bot.get_group_data
	
	bot.get_group_members()
	bot.get_group_member()
	bot.get_group_member_updated()
	bot.get_group_member_deleted()
	bot.get_group_member_added()
	bot.get_group_member_left()
	bot.get_group_member_kicked()
	bot.get_group_member_banned()
	bot.get_group_member_unbanned()
	bot.get_group_member_restricted()
	bot.get_group_member_unrestricted()
	bot.get_group_member_invited()
	bot.get_group_member_promoted()
	bot.get_group_member_demoted()
	
	bot.error()
	
	bot.run()
	
	write data to csv file
	with open('group_data.csv', 'w') as csv_file:
		writer = csv.writer(csv_file)
		for key, value in group_data.items():
			writer.writerow([key, value])
	
	append data to suitable location in csv file (if it exists)
	with open('group_data.csv', 'a') as csv_file:
		writer = csv.writer(csv_file)
		for key, value in group_data.items():
			writer.writerow([key, value])
	
	read data from csv file
	with open('group_data.csv', 'r') as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			print(row)


class SuperTelegramLib(TelegramBot, TelegramLibrary, TelegramModules, TelegramLibraryAndModules,
                       TelegramDataCrawlerBot, MasterClassBijectionBot, MasterFile, MasterFolder, SuperWorkerBot):

	def __init__(self):
		TelegramBot.__init__(self)
		TelegramLibrary.__init__(self)
		TelegramModules.__init__(self)
		TelegramLibraryAndModules.__init__(self)
		TelegramDataCrawlerBot.__init__(self)
		MasterClassBijectionBot.__init__(self)
		MasterFile.__init__(self)
		MasterFolder.__init__(self)
		SuperWorkerBot.__init__(self)   # This is the only one that is not defined anywhere. We need to define it.
async def update_2nd_echo(bot, update_id) -> int:

	if update_id.message.text in chatbot.command_list:

		prob = [1,1,1,1,1,1,1,2,2,2,2,3,3]
		n = random.choice(prob)
		print("choice: ", n)
	
	
	if (n == 0 or chatbot.pause_flag is True) and ("@kerttulibot" not in update.message.text):
		chatbot.wait_user_input(updates.update.message.text)
		time.sleep(2)
		chatbot.answer_user_input(update.message.text)
		return update_id.update_id + 1
	else:
		for i in range(n):
			time.sleep(10/n)
			if "groups" in update.message.text and update.message:
				chatbot.wait_user_input(update.message.text)
				# member = telegram.ChatMember(update.message.chat_id, update.message.from_user.id)
				# chatbot.helper.conversation += f"\n{member}\n"
			elif update.message.text is not None:
				answer = chatbot.answer_user_input(update)
				if "@" in answer:
					await update.message.reply_text(answer, disable_notification=True)
				else:
					print("No answer")
					await bot.send_message(chat_id=update.message.chat_id, text=answer, disable_notification=True)
				logger.info("Sent message %s!", answer)

		return update_id.update_id + 1
		
		


async def update_1st_echo(bot, update_id) -> int:
	"""Echo the user message."""
	try:
		chatbot.wait_user_input(update_id.message.text)
		time.sleep(2)
		chatbot.answer_user_input(update_id.message.text)
		return update_id.update_id + 1
	except Exception as e:
		print(e)
		pass
	except KeyboardInterrupt:
		time.sleep(1)
		pass



if __name__ == '__main__':









# async def main3(bot, update_id):
# 	# Create the EventHandler and pass it your bot's token
# 	# Here we use the `async with` syntax to properly initialize and shutdown resources
# 	# get the first pending update_id, this is so we can skip over it in case
# 	# we get a "Forbidden" exception.
# 	while True:
# 		update_id = await bot.get_updates()[0]
# 		time.sleep(2)
# 		update_id = update_id + 1
# 		try:
# 			update_id = await echo_2(bot, update_id)
# 		except NetworkError:
# 			time.sleep(1)
# 			update_id = update_id
# 		except Forbidden:
# 			# The user has removed or blocked the bot.
# 			update_id += 1
#
# 		try:
# 			update_id = await echo_2(bot, update_id)
# 		except NetworkError:
# 			time.sleep(1)
# 			update_id = update_id
# 		except Forbidden:
# 			# The user has removed or blocked the bot.
# 			update_id += 1
#
# async def main(bot):
# 	"""Run the bot."""
# 	# Create the EventHandler and pass it your bot's token.
# 	# Here we use the `async with` syntax to properly initialize and shutdown resources
# 	# get the first pending update_id, this is so we can skip over it in case
# 	# we get a "Forbidden" exception.
# 	try:
# 		updates = (await bot.get_updates())[0]
# 	except IndexError:
# 		time.sleep(1)
# 		update_id = None
# 	else:
# 		update_id = updates.update_id + 1
# 		logger.info("listening for new messages...")
#
# 	while await updates.update.message.text and updates.update:
# 		print("ALL:", updates.update.message.get_all())
# 		try:
# 			update_id = await echo_2(bot, update_id)
# 			break
# 		except NetworkError:
# 			await asyncio.sleep(1)
# 			update_1st_echo(bot, update_id)
# 			break
# 		except Forbidden:
# 			# The user has removed or blocked the bot.
# 			update_id += 1
#
# 		try:
# 			update_id = await echo_2(bot, update_id)
# 			break
# 		except NetworkError:
# 			await asyncio.sleep(1)
# 			update_1st_echo(bot, update_id)  # repeat with the same update_id
# 		except Forbidden:
# 			# The user has removed or blocked the bot.
# 			update_id += 1
#
# async def main2(bot, update_id):
# 	# Create the EventHandler and pass it your bot's token
# 	# Here we use the `async with` syntax to properly initialize and shutdown resources
# 	# get the first pending update_id, this is so we can skip over it in case
# 	# we get a "Forbidden" exception.
# 	while True:
# 		update_id = await bot.get_updates()[0]
# 		time.sleep(2)
# 		update_id = update_id + 1
# 		try:
# 			update_id = await echo_2(bot, update_id)
# 		except NetworkError:
# 			time.sleep(1)
# 			update_id = update_id
# 		except Forbidden:
# 			# The user has removed or blocked the bot.
# 			update_id += 1
#
# 		try:
# 			update_id = await echo_2(bot, update_id)
# 		except NetworkError:
# 			time.sleep(1)
# 			update_id = update_id
# 		except Forbidden:
# 			# The user has removed or blocked the bot.
# 			update_id += 1
# async def alpha_motor(bot, update_id, updater) -> int:
# 	global id_counter
# 	global update_id_mem
# 	global chatbot
#
# 	for update in await updater.bot.get_updates(offset=update_id, timeout=10):
# 		if update.message:
# 			if update_id.update.message.chat.type == "group":
# 				# if the message is a chatroom info message (not a message from a participant)
# 				# then we skip it
# 				return update_id.update_id + 1
# 			elif update_id.update.message.chat.type == "private":
# 				chatbot.add_conversation(update_id.message.text)
# 				await bot.send_message(chat_id=updater.bot.get_updates(),text=bot.send_message("!"),isable_notification=True)
# 				chatbot.save_conversation()
# 				return update_id.update_id + 1
#
# 	return update_id    # if there are no new messages, then we return the same update_id
#
#
#
# async def echo_2(bot, update_id) -> int:
# 	global id_counter
# 	global update_id_mem
# 	global chatbot
# 	# Request updates after the last update_id
# 	while update_id in await bot.get_updates(offset=update_id, timeout=10):
# 		zippupdate_id = update.update_id + 1
# 		time.sleep(2)
# 		if update.message:  # your bot can receive updates without messages
# 			# Reply to the message
# 			if update.message.text:
# 				chatbot.add_conversation(update.message.text)   # add the message to the conversation
# 				if update.message.chat.type == "group": # if the message is a chatroom info message (not a message from a participant)
# 					# then we skip it
# 					return update_id.update_id + 1
# 				else:
# 					chatbot.add_conversation(update_id.message.text)
# 					bot.send_message(chat_id=update.message.chat_id, text=update.message.text, disable_notification=True)
# 					chatbot.save_conversation()
#
# 	return update_id
#
#
# async def main(bot):
# 	"""Run the bot."""
# 	# Create the EventHandler and pass it your bot's token.
# 	# Here we use the `async with` syntax to properly initialize and shutdown resources.
# 	# TOKEN = get_some()
# 	# async with Bot(TOKEN) as bot:
# 		# get the first pending update_id, this is so we can skip over it in case
# 		# we get a "Forbidden" exception.
# 	while True:
# 		try:
# 			update_id = (await bot.get_updates())[0]
# 		except IndexError:
# 			update_id = None
# 		except Exception as e:
# 			print(e)
# 			update_id = None
#
# 		while update in await bot.get_updates(offset=update_id, timeout=10):
#
# 			update_id += 1
# 			logger.info("listening for new messages...")
#
# 		if await update.message.text:
# 			message = updates.update.message.text
# 			print("ALL:", updates.update.message.get_all())
# 			try:
# 				update_id = await echo_2(bot, update_id)
# 				break
# 			except NetworkError:
# 				await asyncio.sleep(1)
# 				update_1st_echo(bot, update_id)
# 			except Forbidden:
# 				# The user has removed or blocked the bot.
# 				update_id += 1
# 		else:
# 			await update.message.reply_text("I don't understand you.", disable_notification=True)
# 			update_id += 1
# 			logger.info("listening for new messages...")
# 			await asyncio.sleep(1)
# 			update_1st_echo(bot, update_id)
#
# 		# Request updates after the last update_id
# 		for update in await bot.get_updates(offset=update_id, timeout=10):
#
# 			update_id = update.update_id + 1
#
# 			if update.message:
#
# 				if update.message.text:
# 					if update.message.text == "/start":
# 						await update.message.reply_text("Hi!", disable_notification=True)
# 					else:
# 						await update.message.reply_text(update.message.text, disable_notification=True)
# 				else:
# 					await update.message.reply_text("I don't understand you.", disable_notification=True)
# 			else:
# 				await update.message.reply_text("I don't understand you.", disable_notification=True)
# 			update_id += 1
# 			logger.info("listening for new messages...")
# 			await asyncio.sleep(1)
#
#
#
# async def update_1st_echo(bot, update_id) -> int:
#
# 	# Request updates after the last update_id
# 	for update in await bot.get_updates(offset=update_id, timeout=10):
# 		update_id = update.update_id + 1
# 		time.sleep(2)
# 		if update.message.text:
# 			if update.message.text == "/start":
# 				await update.message.reply_text("Hi!", disable_notification=True)
# 			else:
# 				await update.message.reply_text(update.message.text, disable_notification=True)
# 		else:
# 			await update.message.reply_text("I don't understand you.", disable_notification=True)
# 	else:
# 		await update.message.reply_text("I don't understand you.", disable_notification=True)
# 	update_id += 1
# 	logger.info("listening for new messages...")
# 	await asyncio.sleep(1)
# 	return update_id