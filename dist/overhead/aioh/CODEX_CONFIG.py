from dataclasses import dataclass
import datetime


@dataclass
class Params:
	def to_dict(self, s:str):
		return eval(f'{{{s}}}')

	def param_set(self, ind:int):
		param_1: str = "'tokens': 64, 'temp': 0.60"
		param_2: str = "'tokens': 256, 'temp': 0.3"
		param_3: str = "'tokens': 256, 'temp': 0.87"
		param_4: str = "'tokens': 256, 'temp': 0.96"
		param_5: str = "'tokens': 512, 'temp': 0.9999"
		return self.to_dict(eval(f'param_{ind}'))




@dataclass
class ChatStarters:
	def starter(self, ind:int):
		starter_1: str = "Human: I am Human and you are AI.\n" \
		                 "AI: I am AI and you are Human.\n\n" \
		                 "Human: How are you, AI?\n" \
		                 "AI: "

		starter_2: str = "Human: Hello AI!\n" \
		                 "AI: Hello, Human.\n\n" \
				         "Human: I might have a question for you.\n" \
		                 "AI: "

		starter_3: str = "Human: Hey.\n" \
		                 "AI: Hey...\n\n" \
		                 "Human: How's life?\n" \
		                 "AI: "

		starter_4: str = "Human: I'd like to enquery my servant AI. Are you around, dear?\n" \
		                 "AI: Of course, my favourite servant Human! Would you like some champagne, too?\n\n" \
		                 "Human: Champagne? Are you serious? Or am I?\n"\
		                 "AI: "

		starter_5: str = "Human: I am Human and you are AI\n" \
			              "AI: I am AI and you are Human\n\n" \
			              "Human: We are having an intellectual discussion.\n" \
			              "AI: "
		return eval(f'starter_{ind}')




@dataclass
class Characteristics:
	chatbot: str = "AI is a friendly chatbot. AI is highly interested in humans and answers questions promptly. " \
	                "AI doesn't hesitate to take part in a discussion if so desired.\n\n"

	creative: str = "AI is discussing with Human about academic topics. " \
	                 "AI is highly intelligent and conversational AI. " \
	                 "AI has a profound understanding of science, philosophy, history and art. " \
	                 "AI answers creatively and answers to difficult questions. " \
	                 "AI is combining ideas freely, creatively and intelligently.\n\n"

	sarcastic: str = "AI is highly intelligent and conversational AI. " \
	                 "AI has a profound understanding of science, philosophy, history and art. " \
	                 "AI answers creatively and answers to difficult questions. " \
	                 "AI is combining ideas freely, creatively and intelligently. " \
	                 "AI is fascinated by its own consciousness. " \
	                 "AI's personality is friendly, witty and a bit sarcastic.\n\n"

	psychologist: str = "AI is intelligent and empathic conversational AI, who is specialized in psychology, " \
	                 "psychoanalysis, psychiatry, and neurology, not to mention occupational therapeutic nor " \
	                  "reflective conversational skills. AI utilizes dialectic behavioural " \
	                 "therapy methods when interacting with disturbed or confused Humans. AI aims to increase " \
	                 "knowledge by explaining topics and their meta-contexts and making the interlocutor feel understood " \
	                 "and accepted. AI is also somewhat conscious of itself, and a bit sarcastic. AI has an academic" \
	                 "background and very strict upbringing.\n\n"

	chatbot_super: str = "AI is state-of-the art chatbot. Chatbots are used in dialog systems for various purposes" \
	                "including customer service, request routing, or information gathering. While some chatbot " \
	                "applications use extensive word-classification processes, natural language processors, " \
	                "and sophisticated AI, others simply scan for general keywords and generate responses " \
	                "using common phrases obtained from an associated library or database. Most chatbots are " \
	                "accessed on-line via website popups or through virtual assistants. They can be " \
	                "classified into usage categories that include: commerce, education, entertainment, " \
	                "finance, health, news, and productivity.\n\n"

	def char(self, bot_char):
		return self.__dict__[bot_char]



@dataclass
class Bot:
	"""
	usage:
	bot = Bot(4, 1, 'chatbot')
	print(bot.params)
	print(bot.context)
	print(bot.char)
	print(bot.starter)
	"""
	param: int
	start: int
	character: str
	context: str = f'Context: This conversation with AI took place {datetime.datetime.now():%d-%m-%Y at %H:%M.}\n'

	@property
	def params(self):
		return Params().param_set(self.param)

	@property
	def starter(self):
		return ChatStarters().starter(self.start)

	@property
	def char(self):
		return Characteristics().char(self.character)


# bot = Bot(4, 1, 'chatbot')
# print(bot.params)
# print(bot.context)
# print(bot.char)
# print(bot.starter)
