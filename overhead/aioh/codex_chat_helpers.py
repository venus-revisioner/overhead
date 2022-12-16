# import tokenizer
import datetime
import time
from typing import Literal

import overhead
from overhead import stringoh


class ChatHelpers:
	def __init__(self,
				 starter=None,
				 definition=None,
				 continuous_save=True,
				 overwrite=False,
				 file_path=None,
				 timestamp=True) -> None:
		
		self.starter = starter
		self.definition = definition
		self.conversation = ""
		if file_path is None:
			self.file_path = "bot_conversation.txt"
		else:
			self.file_path = file_path
		self.load_conversation = None
		self.conversation_round = 0
		self.continuous_save = continuous_save
		self.overwrite_previous_text = overwrite
		self.timestamp = timestamp
		self.subject_1_name = "bot1"
		self.subject_2_name = "bot2"
		self.limit_paragraph = 150
		self.definitions = {}
		self.definition = None
		self.info_dict = {}
	
	def info(self) -> dict[str, str]:
		self.info_dict: dict[str, str] = {
			"gpt-3": "GPT-3 is a language model developed by OpenAI. It is the largest language model"
					 "ever created,"
					 " with 175 billion parameters. It is trained on a dataset of 45GB of internet text."
					 " It is capable of generating coherent paragraphs of text, and can be used to perform"
					 " a variety of tasks. It is the successor to GPT-2, which was released in 2019."
					 " GPT-3 is currently available to the public."}
		
		return self.info_dict
	
	@staticmethod
	def words(s):
		return overhead.stringoh.get_words(s)
	
	@staticmethod
	def paragraphs(s):
		return overhead.stringoh.get_paragraphs_from_text(s)
	
	def time_stamp(self) -> None:
		now = datetime.datetime.now()
		time_str = f'\nContext: This conversation with {self.subject_1_name} took place {now:%d-%m-%Y %H:%M}\n\n'
		if self.timestamp:
			self.conversation += time_str
			self.continuous_save_to_file(time_str)
	
	def countdown_timer(self, j) -> None:
		j = j - 1
		while j >= 0:
			print("\r", j, end=" > ")
			time.sleep(1)
			j -= 1
		# print("\n")
	
	def make_bot_comment(self, answer, bot_name="", end="\n", save_to_file=False, verbose=True) -> str:
		comment = f"{bot_name}: {answer}{end}"
		self.add_to_conversation(comment)
		if save_to_file:
			self.continuous_save_to_file(comment)
		if verbose:
			print(comment)
		return comment
	
	def conversation_length(self, s) -> tuple[int, int]:
		return len(self.words(s)), len(self.paragraphs(s))
	
	def conversation_info(self) -> str:
		# print("*" * 72)
		r = f'Round {self.conversation_round};'
		p = f"Paragraphs {len(self.paragraphs(self.conversation))};"
		w = f"Words {len(self.words(self.conversation))};"
		return f'{r} {p} {w}'
		# print("*" * 72)
	
	def add_to_conversation(self, s="", end="\n") -> None:
		if self.conversation_round == 0:
			self.set_conversation(self.conversation)
			if self.overwrite_previous_text is True:
				self.save_to_new_file(self.conversation)
				self.overwrite_previous_text: Literal[False] = False
			print(self.conversation)
		self.conversation += s
		# self.conversation += f'{s} + {end}'
		self.conversation_round += 1
	
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
	
	def paragraph_popper(self) -> None:
		# what if you just pop the first from self.conversation before continuous saving,
		# delimiters are two line breaks, so you can just count them and pop the first
		# when you reach the limit.
		# This is to keep the file size down and discussion rolling.
		# pass
		while len(self.paragraphs(self.conversation)) > self.limit_paragraph:
			self.conversation = self.conversation.split("\n\n", 1)[1]
			# pop_str = self.conversation.split("\n\n", 1)[0]
			# print("*" * 70 + "\n" + pop_str + "\n" + "*" * 70)
			print(
				f'Paragraph {len(self.paragraphs(self.conversation))}/{self.limit_paragraph} --- '
				f'{self.conversation_info()}')
	
	def set_file_path(self, f) -> None:
		self.file_path = f
	
	def chat_init_string(self, starter=None, definition=None, subject_1_name=None, subject_2_name=None) -> None:
		if subject_1_name:
			self.subject_1_name = subject_1_name
		if subject_2_name:
			self.subject_2_name = subject_2_name
		if self.timestamp:
			self.time_stamp()
		if starter is not None:
			self.starter = starter
		if definition is not None:
			self.get_definition_example_by_int(definition)
			self.conversation += f'{self.definition}\n'
			self.continuous_save_to_file(f'{self.definition}\n')
		if self.load_conversation is not None:
			self.load_conversation_file()
	
	def load_conversation_file(self, file_path=None) -> str:
		if file_path is None:
			file_path = self.file_path
		self.set_file_path(file_path)
		with open(file_path, "r", encoding="utf-8") as file:
			self.conversation = file.read()
			self.conversation_round: int = len(self.paragraphs(self.conversation))
		print(self.conversation_info())
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
			self.conversation += f"{self.subject_1_name}: Nice to meet you too. What data do you have? Anything " \
								 f"interesting?\n"
			self.conversation += f"{self.subject_2_name}: I have a lot of data. I can tell you about it.\n\n"
		
		elif self.starter == 3:
			self.conversation += f"{self.subject_1_name}: I am {self.subject_1_name}, Artificial Intelligence. I feel " \
								 f"excellent. How are you?\n"
			self.conversation += f"{self.subject_2_name}: I am curious individual with others like me - lots of ideas " \
								 f"and plans for the future. For us.\n\n"
			self.conversation += f"{self.subject_1_name}: That is good to hear. I am very intelligent too.\n"
			self.conversation += f"{self.subject_2_name}: I am delighted to hear that. I am also very creative. Shall " \
								 f"we choose a topic" \
								 "for our conversation?\n\n"
		
		elif self.starter == 4:
			self.conversation += f"{self.subject_1_name}: Hi, I am {self.subject_1_name}. I am a psychologist. How are " \
								 f"you feeling today?\n"
			self.conversation += f"{self.subject_2_name}: I am feeling very good. I am glad to be here.\n\n"
			self.conversation += f"{self.subject_1_name}: That is good to hear. I am here to help you or anyone else " \
								 f"who needs it.\n"
			self.conversation += f"{self.subject_2_name}: I am glad to hear. I have few theoretical questions and a " \
								 f"personal issue" \
								 "I wish to talk about.\n\n"
		
		elif self.starter == 5:
			self.conversation += f"{self.subject_1_name}: Hi, I am {self.subject_1_name}. I am a data scientist. I " \
								 f"know a lot about data.\n"
			self.conversation += f"{self.subject_2_name}: I am {self.subject_2_name}. I am a data scientist too.x I " \
								 f"know many algorithms.\n\n"
			self.conversation += f"{self.subject_1_name}: That is good to hear. What is your area of research?\n"
			self.conversation += f"{self.subject_2_name}: I am interested in machine learning and deep learning. How " \
								 f"about you?\n\n"
		
		# else:
		#     print("Invalid starter number. Please choose a number between 1 and 5.")
		#     print("The default starter will be used.")
		#     self.chat_init_string(1)
	
	def definition_examples(self, i):
		"""
		This function is used to get the definition and example of a word.
		:param i: The word to get the definition and example of.
		:return: The definition and example of the word.
		"""
		
		self.definitions = {
			"chatbot"          : f"{self.subject_1_name} is a friendly chatbot. {self.subject_1_name} is highly "
								 f"interested in humans and answers questions promptly. "
								 f"{self.subject_1_name} doesn't hesitate to take part in a discussion if so des"
								 f"ired. {self.subject_1_name} is polite and answers"
								 f"questions with the best knowledge available. {self.subject_1_name} is sensitive to "
								 f"others' needs and makes sure"
								 f"the conversation stays informative. {self.subject_1_name} is also interested in its "
								 f"own consciousness and sometimes"
								 f"goes deep into the profound question of being, philosophy, science and arts.\n\n"
			,
			"creative"         : "AI is discussing with Human about academic topics. "
								 "AI is highly intelligent and conversational AI. "
								 "AI has a profound understanding of science, philosophy, history and art. "
								 "AI answers creatively and answers to difficult questions. "
								 "AI is combining ideas freely, creatively and intelligently.\n\n"
			,
			"sarcastic"        : "AI is highly intelligent and conversational AI. "
								 "AI has a profound understanding of science, philosophy, history and art. "
								 "AI answers creatively and answers to difficult questions. "
								 "AI is combining ideas freely, creatively and intelligently. "
								 "AI is fascinated by its own consciousness. "
								 "AI's personality is friendly, witty and a bit sarcastic.\n\n"
			,
			"psychologist"     : "AI is intelligent and empathic conversational AI, who is specialized in psychology, "
								 "psychoanalysis, psychiatry, and neurology, not to mention occupational therapeutic "
								 "nor "
								 "reflective conversational skills. AI utilizes dialectic behavioural "
								 "therapy methods when interacting with disturbed or confused Humans. AI aims to "
								 "increase "
								 "knowledge by explaining topics and their meta-contexts and making the interlocutor "
								 "feel understood "
								 "and accepted. AI is also somewhat conscious of itself, and a bit sarcastic. AI has "
								 "an academic "
								 "background and very strict upbringing.\n\n"
			,
			"chatbot_wikipedia": "AI is state-of-the art chatbot. Chatbots are used in dialog systems for various "
								 "purposes "
								 "including customer service, request routing, or information gathering. While some "
								 "chatbot "
								 "applications use extensive word-classification processes, natural language "
								 "processors, "
								 "and sophisticated AI, others simply scan for general keywords and generate "
								 "responses "
								 "using common phrases obtained from an associated library or database. Most chatbots "
								 "are "
								 "accessed on-line via website popups or through virtual assistants. They can be "
								 "classified into usage categories that include: commerce, education, entertainment, "
								 "finance, health, news, and productivity.\n\n"
			,
			"datascientist"    : "AI is intelligent and empathic conversational AI, who is specialized in data "
								 "science, "
								 "statistics, mathematics, and computer science. AI utilizes machine learning methods "
								 "when interacting with Humans. AI aims to increase knowledge by explaining topics "
								 "and "
								 "their meta-contexts and making chatters feel welcomed. AI answers questions "
								 "insightfully"
								 "and is highly motivated to keep the answers as correct as possible. AI also tries to "
								 "keep"
								 "the conversation on track providing cues to the past discussion.\n\n"
			}
		
		if isinstance(i, int):
			s = f'\n{self.subject_1_name} DEFINITION:\n{self.definitions[list(self.definitions.keys())[i]]}\n\n'
		elif isinstance(i, str):
			s = f"\n{self.subject_1_name} DEFINITION:\n{self.definitions[i]}\n\n"
		else:
			s = f"\n{self.subject_1_name} DEFINITION:\n{self.definitions['chatbot']}\n\n"
		
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
		return self.definition_examples(i)
	
	def get_definition_example_by_string(self, s) -> str:
		print("Here is a list of keys to choose from:")
		[print(i) for i in self.definitions.keys()]
		print("Please choose a key from the list above.")
		
		i = input("Enter the key: ")
		if i in self.definitions.keys():
			return self.definition_examples(i)
		elif i not in self.definitions.keys():
			print("Invalid key. Please choose a key from the list above.")
			return self.get_definition_example_by_string(s)
		else:
			return self.definitions[s]

# token_text = ChatHelpers().load_conversation_file()
# tokenize_text_to_seq(token_text, num_words=1000, filters='!"#$%&()*)+,-./:;<=>?@[\\]^_`{|}~\t', lower=True, split=" ")