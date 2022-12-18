# Eplain the code below. It has something to do with secrecy, but I don't understand it.


#         if self.human_writes is None:
#             self.human_writes = True
#             self.helper.chat_init_string(self.starter, self.definition, self.subject_1_name, self.subject_2_name)
#             self.helper.chat_add_string(self.subject_1_name, user_comment, user_name) # add user comment to chat
#             self.helper.chat_add_string(self.subject_2_name, self.bot1.get_response(user_comment), self.subject_2_name) # add bot response to chat
#             self.helper.paragraph_popper()
#             self.human_writes = False
#             return self.bot1.get_response(user_comment)
#         else:
#             self.human_writes = True  # human writes
#             self.helper.chat_add_string(self.subject_1_name, user_comment, user_name) # add user comment to chat
#             self.helper.chat_add_string(self.subject_2_name, self.bot1.get_response(user_comment), self.subject_2_name) # add bot response to chat
#             self.helper.paragraph_popper()
#             self.human_writes = False
#             return self.bot1.get_response(user_comment)


# Path: overhead\aioh\_telegram_chat.py
# Compare this snippet from overhead\aioh\telegram_kerttulibot.py:


#         self.bot1 = None
#         self.subject_1_name = None
#         self.subject_2_name = None
#         self.human_writes: None = None
#
#         self.starter = starter
#         self.definition = definition
#         self.overwrite = overwrite
#         self.continuous_save: bool = continuous_save
#         self.load_file = load
#         self.helper = ChatHelpers(starter, definition, continuous_save, overwrite, load)
#         self.bot1_name: Literal['bot1'] = "bot1"
#         self.bot2_name: Literal['bot2'] = "bot2"
#         self.bot1 = ChatBot(self.bot1_name, storage_adapter="chatterbot.storage.SQLStorageAdapter")
#         self.bot2 = ChatBot(self.bot2_name, storage_adapter="chatterbot.storage.SQLStorageAdapter")
#         self.subject_1_name = "kerttulibot"

# Path: overhead\aioh\_telegram_chat.py
# Compare this snippet from overhead\aioh\telegram_kerttulibot.py:


#         self.bot1 = None
#         self.subject_1_name = None
#         self.subject_2_name = None
#         self.human_writes: None = None
#         self.starter = starter
#         self.definition = definition
#         self.overwrite = overwrite
#         self.continuous_save: bool = continuous_save
#         self.load_file = load
#         self.helper = ChatHelpers(starter, definition, continuous_save, overwrite, load)
#         self.bot1_name: Literal['bot1'] = "bot1"
#         self.bot2_name: Literal['bot2'] = "bot2"
#         self.bot1 = ChatBot(self.bot1_name, storage_adapter="chatterbot.storage.SQLStorageAdapter")
#         self.bot2 = ChatBot(self.bot2_name, storage_adapter="chatterbot.storage.SQLStorageAdapter")
#         self.subject_1_name = "kerttulibot"
#         self.subject_2_name = "group_chat"
#         self.human_writes = True
#         self.helper.chat_init_string(self.starter, self.definition, self.subject_1_name, self.subject_2_name)
#         self.helper.chat_add_string(self.subject_1_name, self.bot1.get_response(self.starter), self.subject_1_name)
#         self.helper.chat_add_string(self.subject_2_name, self.bot2.get_response(self.starter), self.subject_2_name)
#         self.helper.paragraph_popper()
#         self.human_writes = False

# Path: overhead\aioh\_telegram_chat.py
# Compare this snippet from overhead\aioh\telegram_kerttulibot.py:


#         self.bot1 = None
#         self.subject_1_name = None
#         self.subject_2_name = None
#         self.human_writes: None = None
#         self.starter = starter
#         self.definition = definition
#         self.overwrite = overwrite
#         self.continuous_save: bool = continuous_save
#         self.load_file = load
#         self.helper = ChatHelpers(starter, definition, continuous_save, overwrite, load)
#         self.bot1_name: Literal['bot1'] = "bot1"
#         self.bot2_name: Literal['bot2'] = "bot2"
#         self.bot1 = ChatBot(self.bot1_name, storage_adapter="chatterbot.storage.SQLStorageAdapter")
#         self.bot2 = ChatBot(self.bot2_name, storage_adapter="chatterbot.storage.SQLStorageAdapter")
#         self.subject_1_name = "kerttulibot"
#         self.subject_2_name = "group_chat"
#         self.human_writes = True
#         self.helper.chat_init_string(self.starter, self.definition, self.subject_1_name, self.subject_2_name)
#         self.helper.chat_add_string(self.subject_1_name, self.bot1.get_response(self.starter), self.subject_1_name)
#         self.helper.chat_add_string(self.subject_2_name, self.bot2.get_response(self.starter), self.subject_2_name)
#         self.helper.paragraph_popper()
#         self.human_writes = False
#         self.helper.chat_add_string(self.subject_1_name, self.bot1.get_response(self.definition), self.subject_1_name)
#         self.helper.chat_add_string(self.subject_2_name, self.bot2.get_response(self.definition), self.subject_2_name)
#         self.helper.paragraph_popper()
#         self.human_writes = False

# Path: overhead\aioh\_telegram_chat.py
# Compare this snippet from overhead\aioh\telegram_kerttulibot.py:


#         self.bot1 = None
#         self.subject_1_name = None
#         self.subject_2_name = None
#         self.human_writes: None = None
#         self.starter = starter
#         self.definition = definition
#         self.overwrite = overwrite
#         self.continuous_save: bool = continuous_save
#         self.load_file = load
#         self.helper = ChatHelpers(starter, definition, continuous_save, overwrite, load)
#         self.bot1_name: Literal['bot1'] = "bot1"
#         self.bot2_name: Literal['bot2'] = "bot2"
#         self.bot1 = ChatBot(self.bot1_name, storage_adapter="chatterbot.storage.SQLStorageAdapter")
#         self.bot2 = ChatBot(self.bot2_name, storage_adapter="chatterbot.storage.SQLStorageAdapter")
#         self.subject_1_name = "kerttulibot"
#         self.subject_2_name = "group_chat"
#         self.human_writes = True
#         self.helper.chat_init_string(self.starter, self.definition, self.subject_1_name, self.subject_2_name)
#         self.helper.chat_add_string(self.subject_1_name, self.bot1.get_response(self.starter), self.subject_1_name)
#         self.helper.chat_add_string(self.subject_2_name, self.bot2.get_response(self.starter), self.subject_2_name)
#         self.helper.paragraph_popper()
#         self.human_writes = False
#         self.helper.chat_add_string(self.subject_1_name, self.bot1.get_response(self.definition), self.subject_1_name)
#         self.helper.chat_add_string(self.subject_2_name, self.bot2.get_response(self.definition), self.subject_2_name)
#         self.helper.paragraph_popper()
#         self.human_writes = False
#         self.helper.chat_add_string(self.subject_1_name, self.bot1.get_response(self.definition), self.subject_1_name)
#         self.helper.chat_add_string(self.subject_2_name, self.bot2.get_response(self.definition), self.subject_2_name)
#         self.helper.paragraph_popper()
#         self.human_writes = False

# Path: overhead\aioh\_telegram_chat.py
# Compare this snippet from overhead\aioh\telegram_kerttulibot.py:


#         self.bot1 = None

# Path: overhead\aioh\_telegram_chat.py
# Compare this snippet from overhead\aioh\telegram_kerttulibot.py:


#         self.bot1 = None
#         self.subject_1_name = None
#         self.subject_2_name = None
#         self.human_writes: None = None
#         self.starter = starter
#         self.definition = definition
#         self.overwrite = overwrite
#         self.continuous_save: bool = continuous_save
#         self.load_file = load
#         self.helper = ChatHelpers(starter, definition, continuous_save, overwrite, load)
#         self.bot1_name: Literal['bot1'] = "bot1"
#         self.bot2_name: Literal['bot2'] = "bot2"
#         self.bot1 = ChatBot(self.bot1_name, storage_adapter="chatterbot.storage.SQLStorageAdapter")
#         self.bot2 = ChatBot(self.bot2_name, storage_adapter="chatterbot.storage.SQLStorageAdapter")
#         self.subject_1_name = "kerttulibot"
#         self.subject_2_name = "group_chat"
#         self.human_writes = True
#         self.helper.chat_init_string(self.starter, self.definition, self.subject_1_name, self.subject_2_name)
#         self.helper.chat_add_string(self.subject_1_name, self.bot1.get_response(self.starter), self.subject_1_name)
#         self.helper.chat_add_string(self.subject_2_name, self.bot2.get_response(self.starter), self.subject_2_name)
#         self.helper.paragraph_popper()
#         self.human_writes = False
#         self.helper.chat_add_string(self.subject_1_name, self.bot1.get_response(self.definition), self.subject_1_name)
#         self.helper.chat_add_string(self.subject_2_name, self.bot2.get_response(self.definition), self.subject_2_name)
#         self.helper.paragraph_popper()
#         self.human_writes = False
#         self.helper.chat_add_string(self.subject_1_name, self.bot1.get_response(self.definition), self.subject_1_name)
#         self.helper.chat_add_string(self.subject_2_name, self.bot2.get_response(self.definition), self.subject_2_name)
#         self.helper.paragraph_popper()
#         self.human_writes = False
#         self.helper.chat_add_string(self.subject_1_name, self.bot1.get_response(self.definition), self.subject_1_name)
#         self.helper.chat_add_string(self.subject_2_name, self.bot2.get_response(self.definition), self.subject_2_name)
#         self.helper.paragraph_popper()
#         self.human_writes = False
#         self.helper.chat_add_string(self.subject_1_name, self.bot1.get_response(self.definition), self.subject_1_name)
#         self.helper.chat_add_string(self.subject_2_name, self.bot2.get_response(self.definition), self.subject_2_name)
#         self.helper.paragraph_popper()
#         self.human_writes = False
#         self.helper.chat_add_string(self.subject_1_name, self.bot1.get_response(self.definition), self.subject_1_name)
#         self.helper.chat_add_string(self.subject_2_name, self.bot2.get_response(self.definition), self.subject_2_name)
#         self.helper.paragraph_popper()
#         self.human_writes = False

# Path: overhead\aioh\_telegram_chat.py
# Compare this snippet from overhead\aioh\telegram_kerttulibot.py:


#         self.bot1 = None
#         self.subject_1_name = None
#         self.subject_2_name = None
#         self.human_writes: None = None
#         self.starter = starter
#         self.definition = definition
#         self.overwrite = overwrite
#         self.continuous_save: bool = continuous_save
#         self.load_file = load
#         self.helper = ChatHelpers(starter, definition, continuous_save, overwrite, load)
#         self.bot1_name: Literal['bot1'] = "bot1"
#         self.bot2_name: Literal['bot2'] = "bot2"
#         self.bot1 = ChatBot(self.bot1_name, storage_adapter="chatterbot.storage.SQLStorageAdapter")
#         self.bot2 = ChatBot(self.bot2_name, storage_adapter="chatterbot.storage.SQLStorageAdapter")
#         self.subject_1_name = "kerttulibot"
#         self.subject_2_name = "group_chat"
#         self.human_writes = True
#         self.helper.chat_init_string(self.starter, self.definition, self.subject_1_name, self.subject_2_name)
#         self.helper.chat_add_string(self.subject_1_name, self.bot1.get_response(self.starter), self.subject_1_name)

# Path: overhead\aioh\_telegram_chat.py
# Compare this snippet from overhead\aioh\telegram_kerttulibot.py:


# Path: overhead\aioh\_telegram_chat.py

# Path: overhead\aioh\_telegram_chat.py


# Path: overhead\aioh\_telegram_chat.py

# SO how to use all of the above snippets with our Shakespearean function?
# We need to create a new class that inherits from the ChatHelpers class. Why?
# Because we need to override the chat_add_string method. Why?
# Because we need to add the Shakespearean function to the chat_add_string method.
# So we create a new class that inherits from the ChatHelpers class and override the chat_add_string method.
# Is there something wrong with the function? Yes, it is not a method of the class. Why isn't it a method of the
# class? Does it make better plays? No, it doesn't. It is just a function. So we need to make it a method of the class.
# How do we do that? We need to add the self parameter to the function. Why? Because it is a method of the class.
# So we add the self parameter to the function. Is there something wrong with the function now? Yes, it is not a method of the

# Well lets write the Class totally from the scratch. We need to inherit from the ChatHelpers class. Why? Easy way.
# We need to override the chat_add_string method. Why? Because we need to add the Shakespearean function to the chat_add_string method.
# We need to add the self parameter to the function. Why? Because it is a method of the class. Can't we add first a
# list of people, their personal info and everyhing to make the play too interesting? Yes, we can. But we will do that later.
# So we add the self parameter to the function. Is there something wrong with the function now? Yes, it is not a
# method of the class. Why isn't it a method of the class? Does it make better plays? No, it doesn't. It is just a function.
# I can make it a method of the class. How? By adding the self parameter to the function. Why? Because it is a method of the class.

# so should it be classmethod or staticmethod or property or none of the above? I think it should be none of the
# above. Plain function. Why? Because it is not a method of the class. It is just a function. So we need to make it a method of the class.

# DONE. We have a new class that inherits from the ChatHelpers class and overrides the chat_add_string method. And
# the core idea is to use its functions to drive the conversation and rolling buffer. And we have a new function that
# is a method of the class. And we have a new function that is a method of the class. And we have a new function that
# is a method of the class.

# Path: overhead\aioh\_telegram_chat.py


class KafkaProducer:
	
	def __init__(self, topic, bootstrap_servers):
		self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
		self.topic = topic
	
	def send(self, message):
		self.producer.send(self.topic, message)
	
	def close(self):
		self.producer.close()
		
		class TelegramChatKafkaProducer(KafkaProducer):
	#
	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs):
	#
	# 	self._producer = KafkaProducer(bootstrap_servers='localhost:9092')
	#
	def send(self, message):
		self._producer.send('_telegram_chat', message.encode('utf-8'))
	
	def close(self)
		self._producer.close()


class KafkaConsumer:
	
	def __init__(self, topic, bootstrap_servers):
		self.consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers)
	
	def receive(self):
		for message in self.consumer:
			return message.value.decode('utf-8')
	
	def close(self):
		self.consumer.close()


class TelegramChatKafkaConsumer(KafkaConsumer):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self._consumer = KafkaConsumer('_telegram_chat', bootstrap_servers='localhost:9092')
	
	def receive(self):
		for message in self._consumer:
			return message.value.decode('utf-8')
	
	def close(self):
		self._consumer.close()
	

	def __init__(self, starter, definition, continuous_save, overwrite, load):
		self.starter = starter
		self.definition = definition
		self.overwrite = overwrite
		self.continuous_save: bool = continuous_save
		self.load_file = load
		self.helper = ChatHelpers(starter, definition, continuous_save, overwrite, load)
		self.chat = Chat(self.starter, self.definition, self.continuous_save, self.overwrite, self.load_file)
		self.chat.add_string(self.starter, self.definition, self.starter)
		self.chat.add_string(self.starter, self.definition, self.starter)
		self.chat.add_string(self.starter, self.definition, self.starter)
		self.chat.add_string(self.starter, self.definition, self.starter)
		self.chat.add_string(self.starter, self.definition, self.starter)
		self.chat.add_string(self.starter, self.definition, self.starter)
		self.chat.add_string(self.starter, self.definition, self.starter)
		self.chat.add_string(self.starter, self.definition, self.starter)
		self.chat.add_string(self.starter, self.definition, self.starter)
	
	def chat_add_string(self, string):
		self.chat.add_string(self.starter, self.definition, string)
	
	def chat_get_string(self):
		return self.chat.get_string(self.starter, self.definition)
	
	def chat_save(self):
		self.chat.save()
	
	def chat_load(self):
		self.chat.load()
	
	def chat_clear(self):
		self.chat.clear()
	
	def chat_get_all(self):
		return self.chat.get_all()
	
	def chat_get_all_keys(self):
		return self.chat.get_all_keys()
	
	def chat_get_all_values(self):
		return self.chat.get_all_values()
	
	def chat_get_all_keys_values(self):
		return self.chat.get_all_keys_values()
	
	def chat_get_all_keys_values_as_list(self):
		return self.chat.get_all_keys_values_as_list()
	
	def chat_get_all_keys_values_as_list_of_lists(self):
		return self.chat.get_all_keys_values_as_list_of_lists()


class Chat:
	
	def __init__(self, starter, definition, continuous_save, overwrite, load):
		self.starter = starter
		self.definition = definition
		self.overwrite = overwrite
		self.continuous_save: bool = continuous_save
		self.load_file = load
		self.chat = {}
		self.chat[self.starter] = {}
		self.chat[self.starter][self.definition] = []
		self.chat[self.starter][self.definition].append(self.starter)
		self.chat[self.starter][self.definition].append(self.starter)
		self.chat[self.starter][self.definition].append(self.starter)
	
	def add_string(self, starter, definition, string):
		if starter not in self.chat:
			self.chat[starter] = {}
		if definition not in self.chat[starter]:
			self.chat[starter][definition] = []
		if string not in self.chat[starter][definition]:
			self.chat[starter][definition].append(string)
		if self.continuous_save:
			self.save()
	
	def get_string(self, starter, definition):
		if starter in self.chat:
			if definition in self.chat[starter]:
				return random.choice(self.chat[starter][definition])
			else:
				return self.starter
		else:
			return self.starter
	
	def save(self):
		with open(self.load_file, 'w') as file:
			json.dump(self.chat, file)  # , indent=4)
	
	def load(self):
		with open(self.load_file, 'r') as file:
			self.chat = json.load(file)
	
	def clear(self):
		self.chat = {}
		self.chat[self.starter] = {}
		self.chat[self.starter][self.definition] = []
		self.chat[self.starter][self.definition].append(self.starter)
		self.chat[self.starter][self.definition].append(self.starter)
	
	def get_all(self):
		return self.chat
	
	def get_all_keys(self):
		return self.chat.keys()
	
	def get_all_values(self):
		return self.chat.values()
	
	def get_all_keys_values(self):
		return self.chat.items()
	
	def get_all_keys_values_as_list(self):
		return list(self.chat.items())
	
	def get_all_keys_values_as_list_of_lists(self):
		return list(self.chat.items())


class ChatBot:
	
	def __init__(self, token, chat_helpers):
		self.token = token
		self.chat_helpers = chat_helpers
		self.chat_helpers.chat_load()
		self.chat_helpers.chat_save()
	
	def start(self):
		self.updater = Updater(self.token, use_context=True)
		self.dispatcher = self.updater.dispatcher
		self.dispatcher.add_handler(CommandHandler('start', self.start_command))
		self.dispatcher.add_handler(CommandHandler('help', self.help_command))
		self.dispatcher.add_handler(CommandHandler('chat', self.chat_command))
		self.dispatcher.add_handler(CommandHandler('chat_add', self.chat_add_command))
		self.dispatcher.add_handler(CommandHandler('chat_clear', self.chat_clear_command))
		self.dispatcher.add_handler(CommandHandler('chat_save', self.chat_save_command))
		self.dispatcher.add_handler(CommandHandler('chat_load', self.chat_load_command))
		self.dispatcher.add_handler(CommandHandler('chat_get_all', self.chat_get_all_command))
		self.dispatcher.add_handler(CommandHandler('chat_get_all_keys', self.chat_get_all_keys_command))
		self.dispatcher.add_handler(CommandHandler('chat_get_all_values', self.chat_get_all_values_command))
		self.dispatcher.add_handler(CommandHandler('chat_get_all_keys_values', self.chat_get_all_keys_values_command))
		self.dispatcher.add_handler(CommandHandler('chat_get_all_keys_values_as_list', self.chat_get_all_keys_values_as_list_command))
		self.dispatcher.add_handler(CommandHandler('chat_get_all_keys_values_as_list_of_lists', self.chat_get_all_keys_values_as_list_of_lists_command))
		self.dispatcher.add_handler(MessageHandler(Filters.text, self.chat_message))
		self.updater.start_polling()
		self.updater.idle()
	
	def start_command(self, update, context):
		update.message.reply_text('Hi!')
	
	def help_command(self, update, context):
		update.message.reply_text('Help!')
	
	def chat_command(self, update, context):
		update.message.reply_text(self.chat_helpers.chat_get_string(update.message.text, 'chat'))
	
	def chat_add_command(self, update, context):
		self.chat_helpers.chat_add_string(update.message.text, 'chat', update.message.text)
		update.message.reply_text('Added!')
	
	def chat_clear_command(self, update, context):
		self.chat_helpers.chat_clear()
		update.message.reply_text('Cleared!')
	
	def chat_save_command(self, update, context):
		self.chat_helpers.chat_save()
		update.message.reply_text('Saved!')
	
	def chat_load_command(self, update, context):
		self.chat_helpers.chat_load()
		update.message.reply_text('Loaded!')
	
	def chat_get_all_command(self, update, context):
		update.message.reply_text(self.chat_helpers.chat_get_all())
	
	def chat_get_all_keys_command(self, update, context):
		update.message.reply_text(self.chat_helpers.chat_get_all_keys())
	
	def chat_get_all_values_command(self, update, context):
		update.message.reply_text(self.chat_helpers.chat_get_all_values())
	
	def chat_get_all_keys_values_command(self, update, context):
		update.message.reply_text(self.chat_helpers.chat_get_all_keys_values())
	
	def chat_get_all_keys_values_as_list_command(self, update, context):
		update.message.reply_text(self.chat_helpers.chat_get_all_keys_values_as_list())
	
	def chat_get_all_keys_values_as_list_of_lists_command(self, update, context):
		update.message.reply_text(self.chat_helpers.chat_get_all_keys_values_as_list_of_lists())
	
	def chat_message(self, update, context):
		update.message.reply_text(self.chat_helpers.chat_get_string(update.message.text, 'chat'))


def main():
	chat_helpers = ChatHelpers()
	chat_helpers.chat_add_string('hello', 'chat', 'hi')
	chat_helpers.chat_add_string('hi', 'chat', 'hello')
	chat_helpers.chat_add_string('how are you', 'chat', 'fine')
	chat_helpers.chat_add_string('fine', 'chat', 'how are you')
	chat_helpers.chat_add_string('what is your name', 'chat', 'my name is bot')
	chat_helpers.chat_add_string('my name is bot', 'chat', 'what is your name')
	chat_helpers.chat_add_string('what is your name', 'chat', 'my name is bot')
	chat_helpers.chat_add_string('my name is bot', 'chat', 'what is your name')
	chat_helpers.chat_add_string('what is your name', 'chat', 'my name is bot')
	chat_helpers.chat_add_string('my name is bot', 'chat', 'what is your name')