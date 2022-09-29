import os
import openai


def import_file(filepath):
	with open(filepath, 'r') as file:
		query = file.read()
	return query


class CodexClass:
	def __init__(self, temp=0.6, tokens=256, p=1, stop_str="\n\n\n", verbose=0):

		self.filepath = None
		_key = os.getenv("OPENAI_API_KEY").strip("'")
		openai.api_key = _key
		self.prompt, self.response, self.answer = "", "", ""
		self.temperature = temp
		self.max_tokens = tokens
		self.top_p = p
		self.stop = stop_str
		self.verbose = verbose
		self.engine = "code-davinci-001"
		# self.engine = "code-davinci-002"
		# self.engine = "code-cushman-001"
		# self.engine = "code-cushman-002"
		# self.engine = "code-davinci-edit-001"
		# self.engine = "code-cushman-001"
		# self.engine = "text-similarity-babbage-001"
		self.current_path = os.getcwd()
		self.out_file = None
		self.out_file_continued = "codex_class_output.txt"
		self.out_file_path = f'{self.current_path}\\{self.out_file}'
		self.del_chars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
		# self.del_char_smaller = "#$&\'/_()*+:;<=>[]^`{|}~'"+'"'
		self.del_char_smaller = "'\'"

	def prompt_from_file(self, f=None):
		if not f:
			f = self.filepath
		self.prompt = import_file(f)

	def completion(self, s="", verbose=0):
		self.answer = ""
		if s:
			self.prompt = s
		try:
			self.response = openai.Completion.create(engine=self.engine,
													 prompt=self.prompt,
													 temperature=self.temperature,
													 max_tokens=self.max_tokens,
													 top_p=self.top_p,
													 # logprobs=0,
													 frequency_penalty=0,
													 presence_penalty=0,
													 stop=self.stop)

			if verbose:
				print("*" * 40)
				print("Choices:", len(self.response['choices']))
				print(self.response)
				print("*" * 40)

			self.answer = self.response['choices'][0]['text']

			if verbose:
				print(self.answer)

			return self.answer

		except Exception as e:
			print(e)

		except KeyboardInterrupt:
			print("\nKeyboard interruption...\n")
			self.ask_if_save(self.prompt)


	def ask_if_save(self, s):
		print(f'\nDo you want to save this discussion?\n')
		save_question = input("y/n?: ")
		if save_question in "yY, yes":
			with open(self.out_file_path, "w") as f:
				f.write(s)
			print(f'Discussion saved to "{self.out_file_path}".')
			exit()

	def answers(self):
		print(self.answer)

	def print_parameters(self):
		f = f'{self.temperature, self.max_tokens, self.top_p, self.stop}'
		print(f)

	def sanitize(self, s):
		return s.translate({ord(i): "" for i in self.del_char_smaller})
