# docstring... is not here

import os
import sys

class _Cursor:
	def __init__(self):
		self._hide = f'\033[?25l'
		self._show = f'\033[?25h'

	def hide(self):
		# print("hiding cursor...")
		print(self._hide, end="")

	def show(self):
		# print("showing cursor...")
		print(self._show, end="")


class Terminal:
	"""Custom terminal_tools operations."""

	def __init__(self):
		self.terminal_size = None
		self.cursor = _Cursor()

		try:
			term_size = os.get_terminal_size()
			self.terminal_size = term_size.columns, term_size.lines
		except OSError as e:
			print(e)
			print("Try running this script in terminal_tools...")

	def resize(self, cols=80, lines=24):
		try:
			if sys.platform not in "darwin":
				os.system(f'mode con: cols={cols} lines={lines}')
			else:
				os.system(f'resize -s {lines} {cols} >/dev/null')
			# print(f'\nTerminal init size: \t\tcolums={self.terminal_size[0]}, lines={self.terminal_size[1]}')
			# print(f'Terminal resize: \tcolums={cols}, lines={lines}')
		except OSError as e:
			print(e)
			print("Try running this script in terminal_tools...")

	def jump(self, rows=80):
		"""This uses the ANSI escape sequence F,
		which moves to the row above. Add 2 to the rowcount,
		otherwise the top rows will repeat."""
		print("\033[F" * (rows + 2))

	def clear(self):
		if sys.platform not in "darwin":
			os.system('cls')
		else:
			os.system('clear')


def clear_terminal():
	if sys.platform not in "darwin":
		os.system('cls')
	else:
		os.system('clear')


def roll_terminal(rows=60):
	print("\033[F" * (rows + 2))
