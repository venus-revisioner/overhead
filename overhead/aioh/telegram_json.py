

""" This is a sub-function of the function make_dict_without_none_values()
which is used to remove the None values from the dictionary. Moreover, these functions
are used to remove the None values from the dictionary, because the chatbot can not
handle the None values.

In addition, return types are available as list and dictionary, which can be nested.
Moreover, this sub-function handles saving, udpating and deleting the data from the
database. This is done by using the function save_data_to_database() and the function
delete_data_from_database(). Updates are done by using the function update_data_in_database().
Updates are organized based on the update_id. This is done by using the function
get_update_id_from_database(), which relies on the main function get update_id().

In the end this sub-function returns the dictionary without the None values, or list with dictionaries
without the None values, and handles json files, database and the chatbot.
"""
import json
from pprint import pprint

# Now help me organize all these functions as coherent groups, so that I can use them in the main program
# and in the sub-functions of the main program.

# Path: overhead\overhead\aioh\telegram_json.py

# general helper functions and data structures for the chatbot first, and then json files. After that, json file management
# and database management. After that, the main program pipe, or decorators. After that, the main program.

# Path: overhead\overhead\aioh\telegram_json.py

# helper functions for the database

# we define global variables for update_id and next_update_id and update

def get_updates_from_main(data):
	"""
	:param data: data
	:return: update_id, next_update_id, update
	:DESCRIPTION: This function is used to get the update_id, next_update_id and update from the main program
	"""
	# this is the update_id
	update_id = data["update_id"]
	
	# this is the next_update_id
	next_update_id = data["next_update_id"]
	
	# this is the update
	update = data["update"]
	
	return update_id, next_update_id, update


# update_id, next_update_id, update = get_updates_from_main(data)



def get_chat_info(update):
	"""
	:param update: update
	:return: chat_info
	:DESCRIPTION: This function is used to get the chat_info from the update
	"""
	# this IS ONLY placeholder for information which is not available in the update,
	# but is needed for the chatbot, so it is added here, so that the chatbot can use it
	# but if one of the values is not available, it is set to None. How? See below
	
	chat_info = {
		"chat_id                             ": update.message.chat_id,
		"chat_type                           ": update.message.chat.type,
		"chat_title                          ": update.message.chat.title,
		"chat_username                       ": update.message.chat.username,
		"chat_first_name                     ": update.message.chat.first_name,
		"chat_last_name                      ": update.message.chat.last_name,
		"chat_all_members_are_administrators ": update.message.chat.all_members_are_administrators,
		"chat_description                    ": update.message.chat.description,
		"chat_invite_link                    ": update.message.chat.invite_link,
		"chat_pinned_message                 ": update.message.chat.pinned_message,
		"chat_permissions                    ": update.message.chat.permissions,
		"chat_slow_mode_delay                ": update.message.chat.slow_mode_delay,
		"chat_sticker_set_name               ": update.message.chat.sticker_set_name,
		"chat_location                       ": update.message.chat.location,
		"chat_location_address               ": update.message.chat.location.address,
		"chat_location_longitude             ": update.message.chat.location.location.longitude,
		"chat_location_latitude              ": update.message.chat.location.location.latitude,
		"chat_location_horizontal_accuracy   ": update.message.chat.location.location.horizontal_accuracy,
		"chat_location_live_period           ": update.message.chat.location.location.live_period,
		"chat_location_heading               ": update.message.chat.location.location.heading,
		"chat_location_proximity_alert_radius": update.message.chat.location.location.proximity_alert_radius,
		"chat_location_type                  ": update.message.chat.location.location.type,
		"chat_location_id                    ": update.message.chat.location.location.id,
		"chat_location_title                 ": update.message.chat.location.location.title,
		"chat_location_address               ": update.message.chat.location.location.address,
		"chat_location_venue_foursquare_id   ": update.message.chat.location.location.venue_foursquare_id,
		"chat_location_venue_type            ": update.message.chat.location.location.venue_type,
		"chat_location_venue_id              ": update.message.chat.location.location.venue_id,
		"chat_location_venue_title           ": update.message.chat.location.location.venue_title,
		"chat_location_venue_address         ": update.message.chat.location.location.venue_address,
		"chat_location_venue_foursquare_id   ": update.message.chat.location.location.venue_foursquare_id,
		"chat_location_venue_type            ": update.message.chat.location.location.venue_type,
		"chat_location_venue_id              ": update.message.chat.location.location.venue_id,
		"chat_location_venue_title           ": update.message.chat.location.location.venue_title
		
		}
	# this is the part where the None values are removed from the dictionary
	chat_info = make_dict_without_none_values(chat_info)
	return chat_info





# You will get a lot of None values in the dictionary, but that is not a problem, because the chatbot will not use,
# But the program will halt. So, we need to not even access the None values, so we need to pass whenever we encounter a None value
# So, we need to remove the None values from the dictionary. How? See below

def get_message_info(update):
	"""
	:param update: update
	:return: message_info
	:DESCRIPTION: This function is used to get the message_info from the update
	"""
	
	# this IS ONLY placeholder for information which is not available in the update,
	# but is needed for the chatbot, so it is added here, so that the chatbot can use it
	# but if one of the values is not available, it is set to None. How? See below
	
	message_info = {
		"message_id      ": update.message.message_id,
		"date            ": update.message.date,
		"chat            ": update.message.chat,
		"from_user       ": update.message.from_user,
		"from_user_id    ": update.message.from_user.id,
		"from_user_is_bot": update.message.from_user.is_bot,
		"from_user_first_name": update.message.from_user.first_name,
		"from_user_last_name ": update.message.from_user.last_name,
		"from_user_username ": update.message.from_user.username,
		"from_user_language_code": update.message.from_user.language_code,
		"forward_from    ": update.message.forward_from,
		"forward_from_chat": update.message.forward_from_chat,
		"forward_from_message_id": update.message.forward_from_message_id,
		"forward_signature": update.message.forward_signature,
		"forward_sender_name": update.message.forward_sender_name,
		"forward_date    ": update.message.forward_date,
		"reply_to_message": update.message.reply_to_message,
		"edit_date       ": update.message.edit_date,
		"media_group_id  ": update.message.media_group_id,
		"author_signature": update.message.author_signature,
		"text            ": update.message.text,
		"entities        ": update.message.entities,
		"caption_entities": update.message.caption_entities,
		"audio           ": update.message.audio,
		"document        ": update.message.document,
		"animation       ": update.message.animation,
		"game            ": update.message.game,
		"photo           ": update.message.photo,
		"sticker         ": update.message.sticker,
		"video           ": update.message.video,
		"video_note      ": update.message.video_note,
		"voice           ": update.message.voice,
		"caption         ": update.message.caption,
		"contact         ": update.message.contact,
		"location        ": update.message.location,
		"venue           ": update.message.venue,
		"poll            ": update.message.poll
	
		}
	# this is the part where the None values are removed from the dictionary
	
	message_info = make_dict_without_none_values(message_info)
	return message_info


def get_user_info(update):
	"""
	:param update: update
	:return: user_info
	:DESCRIPTION: This function is used to get the user_info from the update
	"""
	
	# this IS ONLY placeholder for information which is not available in the update,
	# but is needed for the chatbot, so it is added here, so that the chatbot can use it
	# but if one of the values is not available, it is set to None. How? See below
	
	user_info = {
		"user_id                                 ": update.message.from_user.id,
		"user_is_bot                             ": update.message.from_user.is_bot,
		"user_first_name                         ": update.message.from_user.first_name,
		"user_last_name                          ": update.message.from_user.last_name,
		"user_username                           ": update.message.from_user.username,
		"user_language_code                      ": update.message.from_user.language_code,
		"user_can_join_groups                    ": update.message.from_user.can_join_groups,
		"user_can_read_all_group_messages        ": update.message.from_user.can_read_all_group_messages,
		"user_supports_inline_queries            ": update.message.from_user.supports_inline_queries,
		"user_chat_id                            ": update.message.chat.id,
		"user_chat_type                          ": update.message.chat.type,
		"user_chat_title                         ": update.message.chat.title,
		"user_chat_username                      ": update.message.chat.username,
		"user_chat_first_name                    ": update.message.chat.first_name,
		"user_chat_last_name                     ": update.message.chat.last_name,
		"user_chat_all_members_are_administrators": update.message.chat.all_members_are_administrators,
		"user_chat_photo                         ": update.message.chat.photo,
		"user_chat_description                   ": update.message.chat.description,
		"user_chat_invite_link                   ": update.message.chat.invite_link,
		"user_chat_pinned_message                ": update.message.chat.pinned_message,
		"user_chat_sticker_set_name              ": update.message.chat.sticker_set_name,
		"user_chat_can_set_sticker_set           ": update.message.chat.can_set_sticker_set,
		"user_chat_location_type                 ": update.message.chat.location.location.type,
		"user_chat_location_id                   ": update.message.chat.location.location.id,
		"user_chat_location_title                ": update.message.chat.location.location.title,
		"user_chat_location_address              ": update.message.chat.location.location.address,
		"user_chat_location_foursquare_id        ": update.message.chat.location.location.venue_foursquare_id,
		"user_chat_location_venue_type           ": update.message.chat.location.location.venue_type,
		"user_chat_location_venue_id             ": update.message.chat.location.location.venue_id,
		"user_chat_location_venue_title          ": update.message.chat.location.location.venue_title,
		"user_chat_location_venue_address        ": update.message.chat.location.location.venue_address,
		"user_chat_location_venue_foursquare_id  ": update.message.chat.location.location.venue_foursquare_id
		}
	
	# this is the part where the None values are removed from the dictionary
	user_info = make_dict_without_none_values(user_info)
	return user_info


def make_dict_without_none_values(dictionary):
	"""
	:param dictionary: dictionary
	:return: dictionary_without_none_values
	:DESCRIPTION: This function is used to remove the None values from the dictionary
	"""
	# this is the dictionary without the None values
	dictionary_without_none_values = {key: value for key, value in dictionary.items() if value is not None}
	
	# this is the list of the values of the dictionary without the None values
	return dictionary_without_none_values



def get_update_id():
	"""
	:return: update_id
	:DESCRIPTION: This function is used to get the update_id from the json file
	:NOTE: This function is not used in the main program
	"""
	with open("update_id.json", "r") as f:
		data = json.load(f)
		update_id = data["update_id"]
	return update_id

def get_update_id_from_update(update):
	"""
	:param update: update
	:return: update_id
	:DESCRIPTION: This function is used to get the update_id from the update
	"""
	update_id = update.update_id
	return update_id


def get_updates(update_id):
	"""
	:return: updates
	:DESCRIPTION: This function is used to get the updates from the telegram bot
	"""
	
	# this is the url for the telegram bot
	url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
	
	# this is the payload for the telegram bot
	payload = {
		"offset ": update_id,
		"timeout": 100
		}
	
	# this is the request for the telegram bot
	r = requests.get(url, params=payload)
	
	# this is the json data from the telegram bot
	data = r.json()
	
	# this is the updates from the telegram bot
	updates = data["result"]
	
	return updates


#---------------JSON MAKING--------------------------------------

def make_json_file_from_dict(dictionary, file_name):
	"""
	:param dictionary: dictionary
	:param file_name: file_name
	:DESCRIPTION: This function is used to make a json file from the dictionary
	"""
	# this is the json file from the dictionary, encoded in utf-8
	with open(file_name, "w", encoding='utf-8') as f:
		json.dump(dictionary, f)


def make_dict_from_json_file(file_name):
	"""
	:param file_name: file_name
	:return: dictionary
	:DESCRIPTION: This function is used to make a dictionary from the json file
	"""
	# this is the dictionary from the json file
	with open(file_name, "r", encoding='utf-8') as f:
		dictionary = json.load(f)
	return dictionary


def make_json_file_from_list(list, file_name):
	"""
	:param list: list
	:param file_name: file_name
	:DESCRIPTION: This function is used to make a json file from the list
	"""
	
	# this is the json file from the list, encoded in utf-8
	with open(file_name, "w", encoding='utf-8') as f:
		json.dump(list, f)


def make_list_from_json_file(file_name):
	"""
	:param file_name: file_name
	:return: list
	:DESCRIPTION: This function is used to make a list from the json file
	"""
	
	# this is the list from the json file. Why not dictionary? Because the json file is a list, and
	# the list is a dictionary, so it is easier to make a list from the json file.
	# Example: the json file is a list of dictionaries, so the list is a dictionary. Every list
	# element is a dictionary, so the list is a dictionary, which contains dictionaries of
	# dictionaries of dictionaries of dictionaries of dictionaries of dictionaries of dictionaries...
	
	with open(file_name, "r", encoding='utf-8') as f:
		list_json = json.load(f)
	return list_json


#---------------DATA HANDLING--------------------------------------

def make_list_from_dict(dictionary):
	"""
	:param dictionary: dictionary
	:return: list
	:DESCRIPTION: This function is used to make a list from the dictionary
	"""
	
	# this is the list from the dictionary
	list_from_dict = [dictionary]
	return list_from_dict


def make_dict_from_list(list_json):
	"""
	:param list: list
	:return: dictionary
	:DESCRIPTION: This function is used to make a dictionary from the list
	@type list_json: object
	"""
	
	# this is the dictionary from the list
	# Example: the json file is a list of dictionaries, so the list is a dictionary. Every list
	# element is a dictionary, so the list is a dictionary, which contains dictionaries of
	# dictionaries of dictionaries of dictionaries of dictionaries of dictionaries of dictionaries...
	
	# why the first one? Because the json file is a list of dictionaries, so the list is a dictionary.
	# How do you separate the dictionaries? You use the first one, because the first one is the first. But you
	# have to use iterator, loop, or recursion to separate the dictionaries. I used recursion. Where?
	# In the function make_dict_without_none_values.
	
	dictionary = list_json[0]
	return dictionary
	

def make_general_abstraction_dict_to_list(list_of_dicts):
	# Is it necessary to make a list of lists from the list of dictionaries? What is deep enough?
	# Cannot it be made on a level of abstraction higher? What is the level of abstraction?
	# It is a general function, which can be used in any case. It is not necessary to make a list
	# of lists from the list of dictionaries, but it is possible. It is not necessary to make a
	# list of lists from the list of lists, but it is possible. But its just plain stupid. Of course
	# you have to make a duality, input output mapping, but not extending the depth of the abstraction.
	
	"""
	:param list_of_dicts: list_of_dicts
	:return: list_of_lists
	:DESCRIPTION: This function is used to make a list of lists from the list of dictionaries
	"""
	
	# make general abstraction from the list of dictionaries
	list_of_lists = []
	for dictionary in list_of_dicts:
		list_of_lists.append(list(dictionary.values()))
	return list_of_lists

def make_general_abstraction_list_to_dict(list_of_lists):
	"""
	:param list_of_lists: list_of_lists
	:return: list_of_dicts
	:DESCRIPTION: This function is used to make a list of dictionaries from the list of lists
	"""
	# make general abstraction from the list of lists
	list_of_dicts = []
	for l in list_of_lists:
		list_of_dicts.append(dict(l))
	return list_of_dicts

def make_general_abstraction_dict_to_dict(dictionarys):
	"""
	:param dictionary: dictionary
	:return: dictionary
	:DESCRIPTION: This function is used to make a dictionary from the dictionary
	"""
	
	# use handy update function, to merge two dictionaries. nested. as many as you want.
	# it is a general function, which can be used in any case. It is not necessary to make a
	
	dictionary = {}
	for d in dictionarys:
		dictionary.update(d)
	return dictionary
	
def make_general_abstraction_list_to_list(lists):
	"""
	:param list: list
	:return: list
	:DESCRIPTION: This function is used to make a list from the list
	"""
	
	# use handy extend function, to merge two lists. nested. as many as you want.
	# it is a general function, which can be used in any case. It is not necessary to make a
	
	list_temp = []
	for l in lists:
		list_temp.extend(l)
	return list_temp



def update_json_file(update_id, next_update_id, file_name):
	"""
	:param update_id: update_id
	:param next_update_id: next_update_id
	:param update: update
	:return: None
	:DESCRIPTION: This function is used to update the json file with the latest update_id and next_update_id
	:NOTE: This function is not used in the main program
	"""
	dictionary = make_dict_from_json_file(file_name)
	update_json_dict = make_general_abstraction_list_to_dict(dictionary)
	update_json_dict = make_dict_without_none_values(make_dict_from_list(update_json_dict))
	pprint(update_json_dict)
	update_json_dict.update(update_id=update_id, next_update_id=next_update_id)
	return update_id, next_update_id


def update_json_file_with_id(update_id, file_name, list_of_dicts):
	# sort the keys and append to the file, based on update_id ascending order
	json_dump = file_name
	update_json_dict = list_of_dicts

	
	with open("update_id.json", "r") as f:
		data = json.load(f)
		update_id = data["update_id"]
		next_update_id = data["next_update_id"]
	return update_id, next_update_id


def update_json_file_with_next_id(next_update_id, file_name, list_of_dicts):
	# sort the keys and append to the file, based on update_id ascending order
	
	json_dump = file_name
	
	update_json_dict = list_of_dicts
	with open("update_id.json", "r") as f:
		data = json.load(f)
		update_id = data["update_id"]
		next_update_id = data["next_update_id"]
	return update_id, next_update_id
	
	
def update_json_file_with_update(update, file_name):
	# sort the keys and append to the file, based on update_id ascending order

	with open(file_name, "r") as f:
		data = json.load(f)
		
	update_json_dict = update.to_dict()

	update_json_dict = {k: v for k, v in update_json_dict.items() if v is not None}
	
	data.append(update_json_dict)
	
	json_dump = json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False, separators= (',', ': '))
	with open(file_name, "w", encoding='utf-8') as f:
		f.write(json_dump)
		f.close()



def update_json_file_with_dicts(update, list_of_dicts):
	
	update_json_dict = list_of_dicts
	update_id = update.update_id
	next_update_id = update.update_id + 1
	
	if update_id is not None and next_update_id is not None:
		if next_update_id == update_id + 1:
			update_json_dict = update.to_dict()
		update_json_dict = {k: v for k, v in update_json_dict.items() if v is not None}
		pprint(update_json_dict)
		
		updating = True
		while updating:
			with open("update.json", "r") as f:
				json_data = json.load(f)
				f.close()
				if json_data["update_id"] == update_id:
					print("updating...")
					with open("update.json", "w") as ff:
						json.dump(update_json_dict, ff, indent=4)
						ff.close()
						updating = False
				else:
					print("not updating...")
					updating = False
		
		# update dict to json
		json_dump = json.dumps(update_json_dict, indent=4)
		with open("update.json", "w") as f:
			f.write(json_dump)
			f.close()
	
	json.dump(update_json_dict, open("update_dict.json", "w", encoding="utf-8"), indent=4, ensure_ascii=True)
	json.dumps(update_json_dict, indent=4, sort_keys=True, default=str, ensure_ascii=True, separators=(",", ": "))



def web_injection(listen_ip, listen_port):
	bot.set_webhook(bot.base_url)
	que = queue.Queue()
	updater = Updater(bot, que)
	# web_bot = telegram.ext.Application(bot=bot,update_queue=que,updater=updater)
	# web_bot.add_handler(CommandHandler("start", start))
	# web_bot.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
	updater.start_webhook(listen=f"{listen_ip}", port=listen_port, url_path=_kerttulibot.TOKEN)
	updater.initialize()
	updater.start_polling(poll_interval=2.0, timeout=10)


def fake():
	
	# get the update_id and next_update_id from the json file
	with open("update_id.json", "r") as f:
		data = json.load(f)
		update_id = data["update_id"]
	
	# get the update from the json file
	with open("update.json", "r") as f:
		update = json.load(f)
		update = telegram.Update.de_json(update, bot)
	
	# get the update_id and next_update_id from the update
	update_id = update.update_id
	next_update_id = update_id + 1
	
	# update the json file with the latest update_id and next_update_id
	update_id, next_update_id = update_json_file(update_id, next_update_id, update)
