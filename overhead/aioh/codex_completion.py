
import argparse
from pathlib import Path
import sys

from CODEX_CONFIG import Bot
from codex_class import CodexClass


def bot_1():
	bot = Bot(3, 1, 'chatbot')
	print(bot.params)
	print(bot.context)
	print(bot.char)
	print(bot.starter)
	return bot.params['temp'], bot.params['tokens'], bot.context + bot.char + bot.starter


def main(args=None):
	temp, tokens, init_str = bot_1()
	if args and args.tokens:
		tokens = args.tokens or 256
	if args and args.temperature:
		temp = args.temp or 0.45

	# override temp and tokens:
	temp, tokens = 0.7, 256

	codex = CodexClass(temp=temp, tokens=tokens, p=1.0, verbose=0)
	if args and args.chat:
		codex.prompt = init_str
	if args and args.ask:
		codex.prompt += codex.sanitize(args.ask)
	if args and args.file:
		codex.prompt_from_file(f=Path(args.file))
	if args is None:
		codex.prompt_from_file(f=Path("codex_prompt_2.py"))

	# codex.prompt = codex.sanitize(codex.prompt)
	# print(codex.prompt)
	codex.completion()
	codex.answers()


if __name__ == "__main__":

	if len(sys.argv) <= 1:
		main(args=None)
	else:
		parser = argparse.ArgumentParser(description="Ask CodexClass.")
		parser.add_argument("--ask","-a", type=str, help="Your input string.")
		parser.add_argument("--tokens","-to", type=int, help="Tokens used total.")
		parser.add_argument("--temperature","-te", type=float, help="Temperament parameter.")
		parser.add_argument("--file","-f", type=str, help="String of file to read as prompt.")

		if (bot.context, bot, char, bot.starter).any() != None:
			parser.add_argument("--chat","-c", type=str, help="Start interactive chat with Codex.")

		args = parser.parse_args()
		main(args)