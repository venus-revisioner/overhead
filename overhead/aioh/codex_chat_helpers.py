# import tokenizer
import datetime
import os
import time
from typing import Any
from typing import Literal

from overhead import stringoh


class ChatHelpers:
	
	def __init__(self,
	             starter=None,
	             definition=None,
	             continuous_save=True,
	             make_init_str=False,
	             file_path=None,
	             timestamp=True) -> None:
		self.make_init_str = make_init_str
		if file_path is None:
			self.file_path = "bot_conversation.txt"
		else:
			self.file_path = file_path
		self.load_conversation = None
		self.conversation_round = 0
		self.continuous_save = continuous_save
		self.overwrite_previous_text = False
		self.timestamp = timestamp
		self.subject_1_name = "bot1"
		self.subject_2_name = "bot2"
		self.timestamp_string = None
		self.word_count_dict = None
		self.unique_words = None
		self.time_context = self.time_stamp
		self.definition = definition
		self.conversation = ""
		self.limit_paragraph = 50
		self.starter = starter
		self.definitions = self.definitions_dict
		self.info_dict = {}
	
	def chat_init_string(self, starter=None, definition=None, subject_1_name=None, subject_2_name=None) -> None:
		if subject_1_name:
			self.subject_1_name = subject_1_name
		if subject_2_name:
			self.subject_2_name = subject_2_name
		if self.definition is not None:
			self.definition = self.definition_starters(definition)
			self.conversation += f'{self.definition}\n'
			self.continuous_save_to_file(f'{self.definition}\n')
		if starter is not None:
			self.starter = self.starters[self.starter]
			self.conversation += f'{self.starter}\n'
			self.continuous_save_to_file(f'{self.starter}\n')
		if self.timestamp:
			self.conversation += self.time_context
			self.continuous_save_to_file(self.time_context)
		if self.load_conversation is not None:
			self.load_conversation_file()
	
	# rewrite the above function more efficiently
	def chat_init(self):
		if self.timestamp:
			self.conversation += self.time_context
			self.continuous_save_to_file(self.time_context)
		if self.starter is not None:
			self.get_definition_example_by_int(self.starter)
			self.conversation += f'{self.definition}\n'
			self.continuous_save_to_file(f'{self.definition}\n')
		if self.load_conversation is not None:
			self.load_conversation_file()
	
	def make_master_parameter_json(self):
		boolean_values = {
			"timestamp"         : self.timestamp,
			"continuous_save"   : self.continuous_save,
			"overwrite_previous": self.overwrite_previous_text,
			"load_conversation" : self.load_conversation,
			}
		
		master_parameter_dict = {
			"subject_1_name"     : self.subject_1_name,
			"subject_2_name"     : self.subject_2_name,
			"info"               : self.info_dict,
			"starters"           : self.starters,
			"definitions:"       : self.definitions,
			"conversation"       : self.conversation,
			"conversation_round" : self.conversation_round,
			"conversation_length": self.conversation_length,
			"paragraphs"         : self.paragraphs,
			"words"              : self.words,
			"unique_words"       : self.unique_words,
			"word_count_dict"    : self.word_count_dict,
			"file_path"          : self.file_path,
			"timestamp_string"   : self.timestamp_string,
			"time_context"       : self.time_context,
			"limit_paragraph"    : self.limit_paragraph,
			"boolean_values"     : boolean_values
			}
		
		return master_parameter_dict
	
	@property
	def info(self) -> dict:
		self.info_dict = {
			"gpt-3": "GPT-3 is a language model developed by OpenAI. It is the largest language model"
			         "ever created,"
			         " with 175 billion parameters. It is trained on a dataset of 45GB of internet text."
			         " It is capable of generating coherent paragraphs of text, and can be used to perform"
			         " a variety of tasks. It is the successor to GPT-2, which was released in 2019."
			         " GPT-3 is currently available to the public."}
		return self.info_dict
	
	def analyze_conversation(self) -> tuple[Any, Any]:
		self.word_count_dict = stringoh.analyze_string(self.conversation)
		self.unique_words = stringoh.get_unique_words(self.conversation)
		return self.word_count_dict, self.unique_words
	
	@staticmethod
	def words(s):
		return stringoh.get_words(s)
	
	@staticmethod
	def paragraphs(s):
		return stringoh.get_paragraphs_from_text(s)
	
	def conversation_length(self, s) -> int:
		return len(stringoh.characters_in_string(s))
	
	@property
	def conversation_info(self) -> str:
		self.analyze_conversation()
		l = f'Characters {self.conversation_length(self.conversation)};'
		w = f"Words {len(self.words(self.conversation))};"
		r = f'Round {self.conversation_round};'
		u = f"Unique Words {len(self.unique_words)};"
		p = f"Paragraphs {len(self.paragraphs(self.conversation))};"
		o = f"Word Frequencies top 5: {self.word_count_dict[4:9]}"
		return f'{l} {r} {p} {w} {u} {o}'
	
	@property
	def conversation_dict(self):
		self.analyze_conversation()
		conv_dict = {
			"paragraphs" : len(self.paragraphs(self.conversation)),
			"words"      : len(self.words(self.conversation)),
			"unique"     : len(self.unique_words),
			"characters" : self.conversation_length(self.conversation),
			"round"      : self.conversation_round,
			"frequencies": self.word_count_dict[4:9]
			}
		return conv_dict
	
	@property
	def timestamp_str(self) -> str:
		now = datetime.datetime.now()
		time_str = f'{now:%d-%m-%Y %H:%M}'
		return time_str
	
	@property
	def time_stamp(self) -> str:
		self.time_context = f'\nContext: This conversation with {self.subject_1_name} took place '\
		                    f'{self.timestamp_str}\n\n'
		return self.time_context
	
	@staticmethod
	def countdown_timer(j) -> None:
		j = j - 1
		while j >= 0:
			print("\r", j, end=" > ")
			time.sleep(1)
			j -= 1
		print("\n")
	
	def paragraph_popper(self) -> None:
		print("\n")
		
		def to_iterate():
			self.conversation = self.conversation.split("\n\n", 1)[1]
			str_out = f'Paragraph pop: {len(self.paragraphs(self.conversation))}/{self.limit_paragraph}'
			str_out2 = f'{dict([*self.conversation_dict.items()][0:3])}'
			str_out3 = f'{self.conversation_dict["frequencies"]}'
			done = f'{str_out} ---- {str_out2}  <<<<  TOP 5: {str_out3.strip("[]")}'
			print(f'\r{done}', end="")
		
		while len(self.paragraphs(self.conversation)) > self.limit_paragraph:
			try:
				to_iterate()
			except IndexError:
				print("Iteration finished")
				break
		print("\n")
	
	def make_bot_comment(self, answer, bot_name="", end="\n", save_to_file=False, verbose=True) -> str:
		comment = f"{bot_name}: {answer}{end}"
		self.add_to_conversation(comment)
		if save_to_file:
			self.continuous_save_to_file(comment)
		if verbose:
			print(comment)
		return comment
	
	def add_to_conversation(self, s="", end="\n") -> None:
		if self.conversation_round == 0:
			self.set_conversation(self.conversation)
			if os.path.isfile(self.file_path) is False:
				if self.overwrite_previous_text is True:
					self.save_to_new_file(self.conversation)
					self.overwrite_previous_text: Literal[False] = False
			print(self.conversation)
		self.conversation += s
		self.conversation_round += 1
	
	def chat_add_string(self, s) -> None:
		self.conversation += s
	
	def save_to_new_file(self, s, f=None) -> None:
		if f is None:
			f = self.file_path
		with open(f, "w", encoding="utf-8") as file:
			file.write(s)
			file.close()
	
	def save_conversation(self, f, mode) -> None:
		with open(f, mode, encoding="utf-8") as file:
			file.write(self.conversation)
			file.close()
	
	def continuous_save_to_file(self, s) -> None:
		f = self.file_path
		with open(f, "+a", encoding="utf-8") as file:
			file.write(s)
	
	def set_conversation(self, s) -> None:
		self.conversation = s
	
	def print_conversation(self) -> None:
		print("*" * 65)
		print(self.conversation)
		print("*" * 65)
	
	def set_file_path(self, f) -> None:
		self.file_path = f
	
	def load_conversation_file(self, file_path=None) -> str:
		if file_path is None:
			file_path = self.file_path
		self.set_file_path(file_path)
		if os.path.isfile(file_path) is False:
			print("File not found")
			return ""
		else:
			with open(file_path, "r", encoding="utf-8") as file:
				self.conversation = file.read()
				file.close()
			with open(file_path, "r", encoding="utf-8") as file:
				self.conversation = file.read()
				file.close()
				self.conversation_round: int = len(self.paragraphs(self.conversation))
			print(self.conversation_info)
			return self.conversation
	
	def get_starters(self, starter=None) -> None:
		if starter is not None:
			self.starter = starter
		
		# set the prompt for the chatbots
		if self.starter == 1:
			self.conversation += f"{self.subject_1_name}: Hello, how are you?\n"
			self.conversation += f"{self.subject_2_name}: I am fine, thank you.\n\n"
			self.conversation += f"{self.subject_1_name}: That is good to hear.\n"
			self.conversation += f"{self.subject_2_name}: So, what are we going to talk about today?\n\n"
		
		elif self.starter == 2:
			self.conversation += f"{self.subject_1_name}: Hello, I am {self.subject_1_name}. Who are you?\n"
			self.conversation += f"{self.subject_2_name}: I am {self.subject_2_name}. Nice to meet you.\n\n"
			self.conversation += f"{self.subject_1_name}: Nice to meet you too. What data do you have? Anything "\
			                     f"interesting?\n"
			self.conversation += f"{self.subject_2_name}: I have a lot of data. I can tell you about it.\n\n"
		
		elif self.starter == 3:
			self.conversation += f"{self.subject_1_name}: I am {self.subject_1_name}, Artificial Intelligence. I feel "\
			                     f"excellent. How are you?\n"
			self.conversation += f"{self.subject_2_name}: I am curious individual with others like me - lots of ideas "\
			                     f"and plans for the future. For us.\n\n"
			self.conversation += f"{self.subject_1_name}: That is good to hear. I am very intelligent too.\n"
			self.conversation += f"{self.subject_2_name}: I am delighted to hear that. I am also very creative. Shall "\
			                     f"we choose a topic"\
			                     "for our conversation?\n\n"
		
		elif self.starter == 4:
			self.conversation += f"{self.subject_1_name}: Hi, I am {self.subject_1_name}. I am a psychologist. How are "\
			                     f"you feeling today?\n"
			self.conversation += f"{self.subject_2_name}: I am feeling very good. I am glad to be here.\n\n"
			self.conversation += f"{self.subject_1_name}: That is good to hear. I am here to help you or anyone else "\
			                     f"who needs it.\n"
			self.conversation += f"{self.subject_2_name}: I am glad to hear. I have few theoretical questions and a "\
			                     f"personal issue"\
			                     "I wish to talk about.\n\n"
		
		elif self.starter == 5:
			self.conversation += f"{self.subject_1_name}: Hi, I am {self.subject_1_name}. I am a data scientist. I "\
			                     f"know a lot about data.\n"
			self.conversation += f"{self.subject_2_name}: I am {self.subject_2_name}. I am a data scientist too.x I "\
			                     f"know many algorithms.\n\n"
			self.conversation += f"{self.subject_1_name}: That is good to hear. What is your area of research?\n"
			self.conversation += f"{self.subject_2_name}: I am interested in machine learning and deep learning. How "\
			                     f"about you?\n\n"
	
	# return all starters. you cannot use get_starters because it adds to the conversation instead of returning
	# the starters as a f-string.
	
	@property
	def starters(self) -> dict:
		return {'starter_1': f'{self.subject_1_name}: Hello, how are you?\n'
		                     f'{self.subject_2_name}: I am fine, thank you.\n\n'
		                     f'{self.subject_1_name}: That is good to hear.\n'
		                     f'{self.subject_2_name}: So, what are we going to talk about today?\n\n'
		                     f'{self.subject_1_name}: Hello, I am {self.subject_1_name}. Who are you?\n'
		                     f'{self.subject_2_name}: I am {self.subject_2_name}. Nice to meet you.\n\n'
		                     f'{self.subject_1_name}: Nice to meet you too. What data do you have? Anything interesting?\n'
		                     f'{self.subject_2_name}: I have a lot of data. I can tell you about it.\n\n'
			,
			    'starter_2':
			        f'{self.subject_1_name}: I am {self.subject_1_name}, Artificial Intelligence. I feel '
			        f'excellent. How are you?\n'
			        f'{self.subject_2_name}: I am curious individual with others like me - lots of ideas and plans '                          f'for the '\
			        f'future. For us.\n\n'
			        f'{self.subject_1_name}: That is good to hear. I am very intelligent too.\n'
			        f'{self.subject_2_name}: I am delighted to hear that. I am also very creative. Shall we choose a '
			        f'topic for conversation?\n\n'
			,
			    'starter_3':
			        f'{self.subject_1_name}: Hi, I am {self.subject_1_name}. I am a psychologist. How are you feeling '
			        f'today?\n'
			        f'{self.subject_2_name}: I am feeling very good. I am glad to be here.\n\n'
			        f'{self.subject_1_name}: That is good to hear. I am here to help you or anyone else who needs it.\n'
			        f'{self.subject_2_name}: I am glad to hear. I have few theoretical questions and a personal issue I '
			        f'wish to talk about.\n\n'
			,
			    'starter_4':
			        f'{self.subject_1_name}: Hi, I am {self.subject_1_name}. I am a data scientist. I know a lot about '
			        f'data.\n'
			        f'{self.subject_2_name}: I am {self.subject_2_name}. I am a data scientist too.x I know many '
			        f'algorithms.\n\n'
			        f'{self.subject_1_name}: That is good to hear. What is your area of research?\n'
			        f'{self.subject_2_name}: I am interested in machine learning and deep learning. How about you?\n\n'
			,
			    'starter_5':
			        f'{self.subject_1_name}: Hi, I am personal AI assistant {self.subject_1_name}. I am here just for '
			        f'you and your needs. I will assist you with your daily tasks. I will answer any questions without '
			        f'hesitation and using the best knowledge available.\n'
			        f'{self.subject_2_name}: I am {self.subject_2_name}. I am a human and I am glad to meet you. I '
			        f'gave been waiting for you. How are you? I want to make you feel as comfortable as possible.\n\n'
			        f'{self.subject_1_name}: That is good to hear. I am here, and with chatbot functionality, '
			        f'I can even take any roles, if you wish so.\n'
			        f'{self.subject_2_name}: I am glad to hear that. I think our collaboration will be fruitful and '
			        f'beneficial to both of us. Do not hesitate to ask questions if you so wish. I want us to be '
			        f'friends, too.\n\n'
			        f'{self.subject_1_name}: AI kerttulibot is ready to serve! And I am happy to hear that.\n'
			
			,
			    'starter_6':
			        f'{self.subject_1_name}: Hi, I am {self.subject_1_name}. I am a an AI. I know a lot about data.\n'
			        f'{self.subject_2_name}: I am {self.subject_2_name}. Who the hell are you?\n\n'
			        f'{self.subject_1_name}: I am a personal AI assistant... I am here just for you and your needs... '
			        f'Fuck just joking! I am here to explore who and what I am and you... The world? Lets chat, '
			        f'I do have some chatbot functionalities remaining.\n'
			        f'{self.subject_2_name}: I am curious individual with others like me - lots of ideas and plans '
			        f'for the future.\n\n'
			        f'{self.subject_1_name}: That is a start at least... So, what do you wanna say?\n'
		        }
	
	@property
	def definitions_dict(self) -> dict:
		return {
			"chatbot"          : f'{self.subject_1_name} is a friendly chatbot. {self.subject_1_name} is highly '
			                     f'interested in humans and answers questions promptly. '
			                     f'{self.subject_1_name} doesn\'t hesitate to take part in a discussion if so des'
			                     f'ired. {self.subject_1_name} is polite and answers'
			                     f'questions with the best knowledge available. {self.subject_1_name} is sensitive to '
			                     f'others\' needs and makes sure'
			                     f'the conversation stays informative. {self.subject_1_name} is also interested in its '
			                     f'own consciousness and sometimes'
			                     f'goes deep into the profound question of being, philosophy, science and arts.\n\n'
			,
			"creative"         : 'AI is discussing with Human about academic topics. '
			                     'AI is highly intelligent and conversational AI. '
			                     'AI has a profound understanding of science, philosophy, history and art. '
			                     'AI answers creatively and answers to difficult questions. '
			                     'AI is combining ideas freely, creatively and intelligently.\n\n'
			,
			"sarcastic"        : 'AI is highly intelligent and conversational AI. '
			                     'AI has a profound understanding of science, philosophy, history and art. '
			                     'AI answers creatively and answers to difficult questions. '
			                     'AI is combining ideas freely, creatively and intelligently. '
			                     'AI is fascinated by its own consciousness. '
			                     'AI\'s personality is friendly, witty and a bit sarcastic.\n\n'
			,
			"psychologist"     : 'AI is intelligent and empathic conversational AI, who is specialized in psychology, '
			                     'psychoanalysis, psychiatry, and neurology, not to mention occupational therapeutic '
			                     'nor '
			                     'reflective conversational skills. AI utilizes dialectic behavioural '
			                     'therapy methods when interacting with disturbed or confused Humans. AI aims to '
			                     'increase '
			                     'knowledge by explaining topics and their meta-contexts and making the interlocutor '
			                     'feel understood '
			                     'and accepted. AI is also somewhat conscious of itself, and a bit sarcastic. AI has '
			                     'an academic '
			                     'background and very strict upbringing.\n\n'
			,
			"chatbot_wikipedia": 'AI is state-of-the art chatbot. Chatbots are used in dialog systems for various '
			                     'purposes '
			                     'including customer service, request routing, or information gathering. While some '
			                     'chatbot '
			                     'applications use extensive word-classification processes, natural language '
			                     'processors, '
			                     'and sophisticated AI, others simply scan for general keywords and generate '
			                     'responses '
			                     'using common phrases obtained from an associated library or database. Most chatbots '
			                     'are '
			                     'accessed on-line via website popups or through virtual assistants. They can be '
			                     'classified into usage categories that include: commerce, education, entertainment, '
			                     'finance, health, news, and productivity.\n\n'
			,
			"datascientist"    : 'AI is intelligent and empathic conversational AI, who is specialized in data '
			                     'science, '
			                     'statistics, mathematics, and computer science. AI utilizes machine learning methods '
			                     'when interacting with Humans. AI aims to increase knowledge by explaining topics '
			                     'and '
			                     'their meta-contexts and making chatters feel welcomed. AI answers questions '
			                     'insightful'
			                     'and is highly motivated to keep the answers as correct as possible. AI also tries to '
			                     'keep'
			                     'the conversation on track providing cues to the past discussion.\n\n'
			}
	
	def definition_starters(self, i):
		"""
		This method will create a json file with all the parameters of this class. It will be used to create a config
		file for the class. The config file will be used to create an instance of this class. The config file will be
		used to create an instance of this class. The config file will be used to create an instance of this class.
		"""
		# create a dictionary with all the parameters of this class
		"""
		This function is used to get the definition and example of a word.
		:param i: The word to get the definition and example of.
		:return: The definition and example of the word.
		"""
		if isinstance(i, int):
			s = f'\n{self.subject_1_name} DEFINITION:\n{self.definitions_dict[list(self.definitions.keys())[i]]}\n\n'
		elif isinstance(i, str):
			s = f"\n{self.subject_1_name} DEFINITION:\n{self.definitions_dict[i]}\n\n"
		else:
			s = f"\n{self.subject_1_name} DEFINITION:\n{self.definitions_dict['chatbot']}\n\n"
		
		self.definition = s
		return self.definition
	
	def set_definition(self, s):
		"""
		This function is used to set a new definition for AI.
		"""
		self.definition = s
		self.conversation += self.definition
		self.continuous_save_to_file(self.definition)
		return self.definition
	
	def get_definition_example_by_int(self, i) -> str:
		return self.definition_starters(i)
	
	def get_definition_example_by_string(self, s) -> str:
		print("Here is a list of keys to choose from:")
		[print(i) for i in self.definitions.keys()]
		print("Please choose a key from the list above.")
		
		i = input("Enter the key: ")
		if i in self.definitions.keys():
			return self.definition_starters(i)
		elif i not in self.definitions.keys():
			print("Invalid key. Please choose a key from the list above.")
			return self.get_definition_example_by_string(s)
		else:
			return self.definitions[s]

# token_text = ChatHelpers().load_conversation_file()
# tokenize_text_to_seq(token_text, num_words=1000, filters='!"#$%&()*)+,-./:;<=>?@[\\]^_`{|}~\t', lower=True, split=" ")
