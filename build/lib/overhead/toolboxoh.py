# coding=utf-8

import os
import sys
import time
from datetime import datetime
import logging
import threading
import math
from itertools import product

from pathlib import Path
import signal

import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as la

from PIL import Image, ImageOps, ImageEnhance

from overhead.decooh import separator, boxed, headline, topic, bordered


class PermuteBruteForce:
	""" Use 'with_function' method, insert your function.
	It maps permutations of this Classes input lists as arguments and loops them. """

	def __init__(self, array_pool=((0, 1), (0, 1)), verbose=1):
		self.array_pool = product(*array_pool)
		self.array_pool_permuted = list(self.array_pool)
		if verbose == 1:
			print('PERMUTED LIST LENGTH:', len(self.array_pool_permuted))

	def with_function(self, func):
		a = map(func, self.array_pool_permuted)
		list(iter(a))

	@property
	def permuted(self):
		return self.array_pool_permuted


class DPICalculator:

	def __init__(self, dpi=300, res=(1200, 1800), size=(20, 30), use_format="metric"):
		'''Standard resolution for printed images:
		dpi = 300
		dpi_300_resolution = 1200, 1800
		dpi_300_res_coeff = 4, 6

		Most online and retail shops have frames this size:
		standard_print_size = 11, 14'''

		# dpi_calc = DPICalculator(dpi=300,res=(4096, 4096),size=(50,50), use_format="metric")
		# dpi_calc.calc_all()
		# dpi_calc.max_size(dpi=300, res=(8192,8192), output_format="cm")
		# dpi_calc.max_reso(dpi=300, size=(100,100), input_format="cm")
		# dpi_calc.min_dpi(res=(3640,1600), size=(21,9), input_format="cm")

		self.dpi = dpi  # DPI stands for dots per inch
		self.dpi_large_format = 100
		self.dpi_web_page_standard = 72
		self.res = res
		self.size = size
		self.use_format = use_format
		self.format_dict = {"metric": "cm", "imperial": "inches"}
		self.standard_print_size = 11, 14

	def inch_to_cm(self, val):
		if isinstance(val, float) or isinstance(val, int):
			return val * 2.54
		if isinstance(val, tuple) or isinstance(val, list):
			return val[ 0 ] * 2.54, val[ 1 ] * 2.54

	def cm_to_inch(self, val):
		if isinstance(val, float) or isinstance(val, int):
			return val / 2.54
		if isinstance(val, tuple) or isinstance(val, list):
			return val[ 0 ] / 2.54, val[ 1 ] / 2.54

	def max_size(self, dpi=None, res=None, output_format="cm"):
		if dpi is None:
			dpi = self.dpi
		if res is None:
			res = self.res
		if output_format is None:
			output_format = self.use_format

		as_inches = res[ 0 ] / dpi, res[ 1 ] / dpi
		size = 0, 0

		if output_format in ("metric", "cm"):
			size = self.inch_to_cm(as_inches)
			output_format = "metric"

		elif output_format in ("imperial", "inch", "inches"):
			size = as_inches
			output_format = "imperial"

		s1 = f'Max. canvas size:\n  - {dpi} DPI\n  - resolution: {res[ 0 ]}px x {res[ 1 ]}px'
		s2 = f' ===>  {size[ 0 ]:.1f} {self.format_dict[ output_format ]} x {size[ 1 ]:.1f} ' \
		     f'{self.format_dict[ output_format ]}'
		# s_out = f'{s1}\n{s2:^{len(s1)-2}}'
		s_out = f'{s1}\n\n{s2}'
		print(s_out)

	def max_reso(self, dpi=None, size=None, input_format="cm"):
		if dpi is None:
			dpi = self.dpi
		if size is None:
			size = self.size
		if input_format is None:
			input_format = self.use_format

		as_inches = 0, 0
		if input_format in ("metric", "cm"):
			as_inches = self.cm_to_inch(size)
			input_format = "metric"

		elif input_format in ("imperial", "inch", "inches"):
			as_inches = size
			input_format = "imperial"

		res = int(as_inches[ 0 ] * dpi), int(as_inches[ 1 ] * dpi)
		difference_percentage = ((((res[ 0 ] * res[ 1 ]) / (self.res[ 0 ] * self.res[ 1 ]))) - 1.) * 100.
		if difference_percentage >= 0.:
			difference_percentage = f'+{difference_percentage:.1f} % more pixels needed'
		else:
			difference_percentage = f'{difference_percentage:.1f} % below maximum'

			s1 = f'Max. resolution:\n  - {dpi} DPI\n  - size: {size[ 0 ]:.1f} {self.format_dict[ input_format ]} x ' \
			     f'{size[ 1 ]:.1f} {self.format_dict[ input_format ]}'
			s2 = f' ===>  {res[ 0 ]}px x {res[ 1 ]}px\n\n  {difference_percentage}'
			s_out = f'{s1}\n\n{s2}'
			# s_out = f'{s1}\n{s2:^{len(s1)-2}}'
			print(s_out)


def min_dpi(self, res=None, size=None, input_format="cm"):
	if res is None:
		res = self.res
	if size is None:
		size = self.size
	if input_format is None:
		input_format = self.use_format

	as_inches = 0, 0
	if input_format in ("metric", "cm"):
		as_inches = self.cm_to_inch(size)
		input_format = "metric"

	elif input_format in ("imperial", "inch", "inches"):
		as_inches = size
		input_format = "imperial"

		dpi = int(res[ 0 ] / as_inches[ 0 ]), int(res[ 1 ] / as_inches[ 1 ])

		s1 = f'Min. DPI required:\n  - for resolution {res[ 0 ]}px x {res[ 1 ]}px\n  - with' \
		     f' size {size[ 0 ]:.1f} {self.format_dict[ input_format ]} x {size[ 1 ]:.1f} ' \
		     f'{self.format_dict[ self.use_format ]}'
		s2 = f' ===>  {max(dpi)} DPI\n\n  (Min. of [{dpi[ 0 ]}, {dpi[ 1 ]}])'
		# s_out = f'{s1}\n{s2:^{len(s1)-2}}'
		s_out = f'{s1}\n\n{s2}'
		print(s_out)


def print_params(self):
	print(f'DPI:\t {self.dpi}')
	print(f'Reso:\t {self.res}')
	print(f'Size:\t {self.size}')
	print(f'Format:\t {self.use_format}')


def calc_all(self):
	print("-" * 30)
	self.max_size(self.dpi, self.res, self.use_format)
	print("-" * 30)
	self.max_reso(self.dpi, self.size, self.use_format)
	print("-" * 30)
	self.min_dpi(self.res, self.size, self.use_format)
	print("-" * 30)


class AsciiConverter:

	def __init__(self, norm_str=None, ascii_str=None):
		self.norm_str = norm_str
		self.ascii_str = ascii_str

		if norm_str and not ascii_str:
			self.ascii_str = self.str_to_ascii()
		elif not norm_str and ascii_str:
			self.norm_str = self.ascii_to_str()

	def ascii_variations(self, ascii_str=None, amt=100, offset=97, sum=0, sca=1, mod_val=220):
		if not ascii_str:
			ascii_str = self.ascii_str
		for i in range(amt):
			x = [ (offset + (int(i + k + sum) * sca)) % mod_val for k in ascii_str ]
			print(self.ascii_to_str(x))

	def ascii_to_str(self, ascii_str=None):
		if not ascii_str:
			ascii_str = self.ascii_str
		d = ""
		for i in ascii_str:
			d += chr(i)
		return d

	def str_to_ascii(self, norm_str=None):
		if not norm_str:
			norm_str = self.norm_str
		d = [ ]
		for i in norm_str:
			d.append(ord(i))
		return d


def get_user_name():
	"""Attempt to retrieve logged in username from env."""
	if sys.platform == 'win32':
		user_name = os.getenv('username')
	else:
		user_name = os.getenv('USER')
	return user_name


class QuitSignal:

	def __init__(self):
		signal.signal(signal.SIGINT, self.signal_handler)

	def signal_handler(self, signal, frame):
		print("\nProgram exiting gracefully <3")
		sys.exit(0)


class KeyHandler(threading.Thread):

	def __init__(self, verbose=0, quit_key='q'):
		self.quit_key = quit_key
		self.verbose = verbose
		self.quit_flag = False
		self.user_input = ""
		threading.Thread.__init__(self)

	def run(self):
		while True:
			user_input = input()
			self.user_input = user_input

			if self.verbose:
				print(f'--- Received "{user_input}"')
				self.user_input = user_input

			if self.quit_key in self.user_input:
				self.quit()
				if self.verbose:
					print(f'\n** QUIT KEY "{self.quit_key}" RECEIVED **')

				break
			time.sleep(1)

			if self.user_input != "":
				self.user_input = ""

			if self.quit_flag:
				break

	def quit(self):
		self.quit_flag = True

	def param_map(self, param: dict):
		""" User input: t.ex. variable change: 'x_fade 0.4' (with space between) """
		if self.user_input:
			key_split = self.user_input.split()
			if len(key_split) > 1 and key_split[ 0 ] in param.keys():
				exec(f'{key_split[ 0 ]}={key_split[ 1 ]}')
			size = self.size
			print(f'\n** New Mapping: {key_split[ 0 ]}={key_split[ 1 ]}')


class MyLogging:

	def __init__(self):
		self.level = logging.DEBUG
		# self.ftm = '[%(levelname)s]: %(asctime)s - %(message)s'
		self.ftm = "%(levelname)s:%(name)s:%(message)s"
		# self.ftm = "%(levelname)s:%(asctime)s %(module)s:   '%(message)s'    %(funcName)s"
		# self.ftm = "%(levelname)s:%(module)s:%(funcName)s:%(asctime)s: '%(message)s'"
		# self.ftm = "%(levelname)s:%(name)s:%(module)s:%(threadName)s:%(funcName)s:\n%(asctime)s: '%(message)s'"
		logging.basicConfig(level=self.level, format=self.ftm)


class TimeEval:

	def __init__(self):
		self.start_time = None
		self.end_time = None
		self.total_seconds = None
		self.total_time_str = ""
		self.yearly_dict = dict()
		self.second_decimals = 3

	def start(self):
		self.start_time = time.time()

	def stop(self, verbose=0):
		self.end_time = time.time()
		self.total_seconds = self.end_time - self.start_time
		self.get_time_str(verbose=verbose)
		return self.total_seconds

	def get_time_str(self, verbose=0, prefix="Total time: "):
		self.time_to_human_readable(prefix=prefix)
		if verbose:
			print(self.total_time_str)
		else:
			return self.total_time_str

	def time_to_human_readable(self, seconds=None, prefix="Total time:"):
		"""Input: seconds elapsed. Also, use separately to get nice print up to a year."""

		if seconds is not None:
			self.total_seconds = seconds


class DPICalculator:

	def __init__(self, dpi=300, res=(1200, 1800), size=(20, 30), use_format="metric"):
		'''Standard resolution for printed images:
		dpi = 300
		dpi_300_resolution = 1200, 1800
		dpi_300_res_coeff = 4, 6

		Most online and retail shops have frames this size:
		standard_print_size = 11, 14'''

		# dpi_calc = DPICalculator(dpi=300,res=(4096, 4096),size=(50,50), use_format="metric")
		# dpi_calc.calc_all()
		# dpi_calc.max_size(dpi=300, res=(8192,8192), output_format="cm")
		# dpi_calc.max_reso(dpi=300, size=(100,100), input_format="cm")
		# dpi_calc.min_dpi(res=(3640,1600), size=(21,9), input_format="cm")

		self.dpi = dpi  # DPI stands for dots per inch
		self.dpi_large_format = 100
		self.dpi_web_page_standard = 72
		self.res = res
		self.size = size
		self.use_format = use_format
		self.format_dict = {"metric": "cm", "imperial": "inches"}
		self.standard_print_size = 11, 14

	def inch_to_cm(self, val):
		if isinstance(val, (float, int)):
			return val * 2.54
		if isinstance(val, (tuple, list)):
			return val[ 0 ] * 2.54, val[ 1 ] * 2.54

	def cm_to_inch(self, val):
		if isinstance(val, (float, int)):
			return val / 2.54
		if isinstance(val, (tuple, list)):
			return val[ 0 ] / 2.54, val[ 1 ] / 2.54

	def max_size(self, dpi=None, res=None, output_format="cm"):
		if dpi is None:
			dpi = self.dpi
		if res is None:
			res = self.res
		if output_format is None:
			output_format = self.use_format

		as_inches = res[ 0 ] / dpi, res[ 1 ] / dpi
		size = 0, 0

		if output_format in ("metric", "cm"):
			size = self.inch_to_cm(as_inches)
			output_format = "metric"

		elif output_format in ("imperial", "inch", "inches"):
			size = as_inches
			output_format = "imperial"

		s1 = f'Max. canvas size:\n  - {dpi} DPI\n  - resolution: {res[ 0 ]}px x {res[ 1 ]}px'
		s2 = f' ===>  {size[ 0 ]:.1f} {self.format_dict[ output_format ]} x {size[ 1 ]:.1f} ' \
		     f'{self.format_dict[ output_format ]}'
		# s_out = f'{s1}\n{s2:^{len(s1)-2}}'
		s_out = f'{s1}\n\n{s2}'
		print(s_out)

	def max_reso(self, dpi=None, size=None, input_format="cm", prefix=None):
		if dpi is None:
			dpi = self.dpi
		if size is None:
			self.make_time_dict()
		self.total_time_str = ""
		year_dict_reversed = dict(reversed(list(self.yearly_dict.items())))
		for key, value in year_dict_reversed.items():
			if key != 'sec' and value > 0 or key == 'sec':
				self.total_time_str += f'{value} {key} '
		self.total_time_str = f'{prefix} {self.total_time_str}'

	def make_time_dict(self):
		sec = int(self.total_seconds)
		min = int((self.total_seconds / 60))
		hour = int(min / 60)
		day = int(hour / 24)
		year = int(day / 365.25)

		self.yearly_dict = {'sec': sec % 60, 'min': min % 60, 'hours': hour % 24, 'days': day % 365.25, 'years': year}
		self.yearly_dict[ 'sec' ] = f'{self.total_seconds % 60:.{self.second_decimals}f}'

	@property
	def log_time(self):
		return f'Run on: {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}'


class PerformEval:
	"""Evaluate performance with its start and stop methods. Preferred use case high performance and accuracy."""

	def __init__(self, verbose=1):
		self.start_time = None
		self.end_time = None
		self.verbose = verbose

	def start(self):
		self.start_time = time.perf_counter()

	def stop(self):
		self.end_time = time.perf_counter()

		if self.verbose:
			self.print_time()

	def print_time(self):
		print_boxed(f'Evaluation took {self.end_time - self.start_time:0.7f} sec')


# class _Cursor:
# 	def __init__(self):
# 		self._hide = f'\033[?25l'
# 		self._show = f'\033[?25h'
#
# 	def hide(self):
# 		# print("hiding cursor...")
# 		print(self._hide, end="")
#
# 	def show(self):
# 		# print("showing cursor...")
# 		print(self._show, end="")


# class Terminal:
# 	"""Custom terminal_tools operations."""
#
# 	def __init__(self):
# 		self.terminal_size = None
# 		self.cursor = _Cursor()
#
# 		try:
# 			term_size = os.get_terminal_size()
# 			self.terminal_size = term_size.columns, term_size.lines
# 			print(f'\nTerminal init size: \t\tcolums={self.terminal_size[0]}, lines={self.terminal_size[1]}')
# 		except OSError as e:
# 			print(e)
# 			print("Try running this script in terminal_tools...")
#
# 	def resize(self, cols=80, lines=24):
# 		try:
# 			print(f'Terminal resize: \tcolums={cols}, lines={lines}')
# 			if sys.platform not in "darwin":
# 				os.system(f'mode con: cols={cols} lines={lines}')
# 			else:
# 				os.system(f'resize -s {lines} {cols} >/dev/null')
# 		except OSError as e:
# 			print(e)
# 			print("Try running this script in terminal_tools...")
#
# 	def jump(self, rows=80):
# 		"""This uses the ANSI escape sequence F,
# 		which moves to the row above. Add 2 to the rowcount,
# 		otherwise the top rows will repeat."""
# 		print("\033[F" * (rows + 2))
#
# 	def clear(self):
# 		if sys.platform not in "darwin":
# 			os.system('cls')
# 		else:
# 			os.system('clear')


class _Color:

	def __init__(self):
		from colorama import Fore, Back, Style

		y = list(map(lambda x: x.swapcase().replace("light", "light ").split("_")[ 0 ], Fore.__dict__.keys()))
		z = list(zip(y, Fore.__dict__.values()))
		self.fore_codes = {k: v for k, v in z}

		y = list(map(lambda x: x.swapcase().replace("light", "light ").split("_")[ 0 ], Back.__dict__.keys()))
		z = list(zip(y, Back.__dict__.values()))
		self.back_codes = {k: v for k, v in z}

		y = list(map(lambda x: x.swapcase().replace("_", " "), Style.__dict__.keys()))
		z = list(zip(y, Style.__dict__.values()))
		self.style_codes = {k: v for k, v in z}

	def print_dicts(self):
		print()
		print("fore codes:")
		print(self.fore_codes)
		print()
		print("back codes:")
		print(self.back_codes)
		print()
		print("style codes:")
		print(self.style_codes)
		print()


class ColorizeText(_Color):
	"""
	STYLE: bright, dim, normal
	"""

	def __init__(self):
		self._pre_str = ""
		self._post_str = ""
		self._reset_str = ""

		self._fore = None
		self._back = None
		self._style = None
		self._reset = None

		self._fore_color = ""
		self._back_color = ""
		self._style_style = ""

		_Color.__init__(self)

		self._fore_reset = self.fore_codes[ 'reset' ]
		self._back_reset = self.back_codes[ 'reset' ]
		self._style_reset = self.style_codes[ 'reset all' ]

	# print(self.style_codes['reset all'])

	@property
	def fore(self):
		"""Returns fore color"""
		return self._fore

	@fore.setter
	def fore(self, c):
		self._fore = c
		try:
			self._fore_color = self.fore_codes[ c ]
			self._pre_str += self._fore_color
			self._post_str += self._fore_reset
			self.insta_print(self._fore_color)
		except Exception:
			print("Keyword error, try these instead.")
			self.rainbow()

	@fore.deleter
	def fore(self):
		del self._fore

	@property
	def back(self):
		"""Returns back color"""
		return self._back

	@back.setter
	def back(self, c):
		self._back = c
		try:
			self._back_color = self.back_codes[ c ]
			self._pre_str += self._back_color
			self._post_str += self._back_reset
			self.insta_print(self._back_color)
		except Exception:
			print("Keyword error, try these instead.")
			self.rainbow()

	@back.deleter
	def back(self):
		del self._back

	@property
	def style(self):
		"""Returns color style"""
		return self._style

	@style.setter
	def style(self, c):
		try:
			self._style_style = self.style_codes[ c ]
			self._pre_str += self._style_style
			self._post_str += self._style_style
			self.insta_print(self._style_style)
		except Exception:
			print("Keyword error, try these instead.")
			print(self.style_codes.keys())

	@style.deleter
	def style(self):
		del self._style

	def reset_all(self):
		self._fore = ""
		self._fore_color = ""
		self._back = ""
		self._back_color = ""
		self._style = ""
		self._style_style = ""
		s = self.style_codes[ 'reset all' ]
		self.insta_print(s)
		return s

	def prefix(self):
		s = f'{self._pre_str}'
		self.insta_print(s)
		return s

	def postfix(self):
		s = f'{self._post_str}'
		self.insta_print(s)
		return s

	def colorize(self, s, fore=None, back=None):
		if fore is not None:
			self.fore = fore
		if back is not None:
			self.back = back
		if not self._back_color:
			self._back_color = ""
		if not self._fore_color:
			self._fore_color = ""
		if not self._style_style:
			self._style_style = ""
		x = f'{self._back_color}{self._fore_color}{self._style_style}{s}{self.reset_all()}'
		return x

	def insta_return(self, c):
		return f'{c}'

	def insta_print(self, c):
		print(f'{c}', end="")

	def easy_print(self, s, append=1):
		if not self._back_color:
			self._back_color = ""
		if not self._fore_color:
			self._fore_color = ""
		if not self._style_style:
			self._style_style = ""
		x = f'{self._back_color}{self._fore_color}{self._style_style}{s}{self.reset_all()}'
		if not append:
			print(x)
		else:
			return x

	def rainbow(self, s="RAINBOW"):
		r = self.reset_all()
		for key, value in self.fore_codes.items():
			print(f'{value}{s:10}{key}{r}')

	def rainbow_extended(self, s="!!RAINBOW!!"):
		r = self.reset_all()

		for key, value in self.fore_codes.items():
			for key_2, value_2 in self.back_codes.items():
				c = f'{value}{value_2}'
				k1, k2 = key.swapcase(), key_2.swapcase()
				print(f'{c}{s:13}fore:  {k1:14}{c}  back:  {c}{k2:16}{r}')
				time.sleep(0.02)


def timestamp_convert(time_stamp, get_date=1, get_time=1, date_str="dmy"):
	t = datetime.fromtimestamp(time_stamp / 1e3)
	a, b = "", ""
	if get_date:
		d, m, y = "", "", ""
		if "d" in date_str:
			d = "%d."
		if "m" in date_str:
			m += "%m."
		if "y" in date_str:
			y += "%Y"
		a = t.strftime(f'{d}{m}{y}')
	if get_time:
		b = t.strftime('%H:%M:%S')
	return f'{a} {b}'.strip()


def human_readable_big_number(number):
	if 1e6 > number > 1e3:
		return f'{(number / 1e3):.2f} k'
	elif 1e9 > number >= 1e6:
		return f'{(number / 1e6):.2f} M'
	elif 1e12 > number >= 1e9:
		return f'{(number / 1e9):.2f} B'
	elif 1e15 > number >= 1e12:
		return f'{(number / 1e12):.2f} T'
	else:
		return f'{number:.2f}'


# def print_boxed(*args, **kwargs):
# 	s = ""
# 	for item in args:
# 		s += f' {item}'
# 	pause_str = s
# 	box_len = len(pause_str) + 10
# 	print()
# 	print("-" * box_len)
# 	print("|", " " * 2, pause_str, " " * 2, "|")
# 	print("-" * box_len)
# 	print()

@separator
def print_separator(s, *args, **kwargs):
	# print(s)
	return s


@boxed
def print_boxed(*args, **kwargs):
	print(*args)


@headline
def print_headline(*args, **kwargs):
	print(*args)


@topic
def print_topic(*args, **kwargs):
	print(*args)


@bordered
def print_bordered(*args, **kwargs):
	print(*args)


def print_min_max(item, n=""):
	print(n + " -- min max:", np.min(item).round(4), np.max(item).round(4))


# @bordered
def sleep_counter(countdown=5, countdown_str="!! COUNTDOWN:"):
	for i in range(countdown):
		print(countdown_str, countdown - i, end="\n")
		time.sleep(1)


def flatten_naive(t):
	return [ item for sublist in t for item in sublist ]


def insert_list_at_intervals(list_in, ind, interval, offset):
	a = list_in
	for e, i in enumerate(a):
		a = np.roll(a, -1)
		if (e + offset) % interval == 0:
			for x in ind:
				a = np.append(a, x)

	return a.tolist()


def normalize(array, signed=0):
	if signed:
		array += np.abs(np.amin(array))
		array -= (np.amax(array) / 2.)
		return array
	else:
		array = np.array(array, np.float32) - np.min(array)
		return array / np.max(array)


def scale(oldvalue, oldmin, oldmax, newmin, newmax):
	return (((oldvalue - oldmin) * (newmax - newmin)) / (oldmax - oldmin)) + newmin


def palindrome(arr):
	return arr + arr[ ::-1 ][ 1: ]


def power_scale(b, sca, pow_w, offset=0):
	if type(b) not in (float, int):
		b = np.array(b)
		a = np.power(1 / b, pow_w) * sca
		a = (normalize(a) * (sca - 1)) + offset
		a = a[ ::-1 ]
		return a

	elif type(b) is float or int:
		b = max(b, 0.5)
		b /= (sca)
		a = math.pow(1 / (b), pow_w) - 1
		c = math.pow(1 / (1 / sca), pow_w) - 1
		a *= 1 / c
		a *= (sca - 1)
		a += offset
		return a


# ----Data plotting ------------------------------------------------------------------------


def draw_1d(in_x=None, in_y=None, as_subplot=0):
	x, y = None, None
	if in_x is None or in_y is None:
		x = np.arange(0, 1, 0.01)
		x *= (math.pi * 2.)
		y = np.sin(x)
	else:
		if in_x is not None:
			x = in_x
		if in_y is not None:
			y = in_y

	if as_subplot:
		return x, y

	else:
		print("Drawing")
		plt.plot(x, y)
		plt.show()


def draw_subplots(plots=()):
	fig, ax = plt.subplots(len(plots[ 0 ]))
	fig.suptitle('Vertically stacked subplots')
	for i, p in enumerate(plots):
		ax[ i ].plot(*p)
		ax[ i ].title.set_text("Plot " + str(i + 1))
	plt.subplots_adjust(hspace=0.5)
	plt.show()


def draw_2d(m=None, gray=0, contour=0):
	if m is None:
		g = np.ones((100, 100))
		x = np.arange(0, 100, 1)
		y = np.arange(0, 100, 1)
		x = np.array(x)
		y = np.array(y)
		x = (x / 100) * 2. - 1.
		y = (y / 100) * 2. - 1.

		f = (x * x / 2 + y * y / 2) / np.pi

		g[ :, : ] = 1. - f
		g2 = np.rot90(g)
		g *= g2
		g *= g
		g3 = np.greater_equal(g, 0.5)
		g = g3 * g
		m = g

	if gray:
		plt.gray()

	if contour:
		f = np.sin(x ** 2 + y ** 2) / (x ** 2 + y ** 2)
		h = plt.contourf(m[ 0, : ], m[ :, 0 ], f)
	else:
		plt.imshow(m)
	plt.show()


def draw_2d_contour(x=None, y=None):
	if not x:
		x = np.arange(-4, 4, 0.01)
	else:
		x = normalize(x, signed=1)
	if not y:
		y = np.arange(-4, 4, 0.01)
	else:
		y = normalize(y, signed=1)
	xx, yy = np.meshgrid(x, y, sparse=True)
	z = np.sin(xx ** 2 + yy ** 2) / (xx ** 2 + yy ** 2)
	h = plt.contourf(x, y, z)
	plt.show()


def magnitude_2d(x=None, y=None, show=0):
	c = np.array([ x, y ]).swapaxes(1, 0)
	mag = np.sqrt(la.norm(c, axis=1))
	x_mag = np.linspace(-1., 1., len(mag))
	if show:
		plt.plot(x_mag, mag)
		plt.show()
	return mag


# Work in process...
def simple_matrix(dim=(100, 100), norm=None, s_norm=None, func=None, func_scaler=None, gray=None, return_only_x=None):
	""" f = "1.-((x * x / 2 + y * y / 2) / np.pi)"
		m = simple_matrix(norm=(1.,1.),s_norm=(2.,2.),func_fusion=f)
		draw_function_2d(m) """

	g = np.ones((dim[ 0 ], dim[ 1 ]))

	if func_scaler is not None:
		g *= func_scaler

	x = np.arange(0, dim[ 0 ], 1)
	y = np.arange(0, dim[ 1 ], 1)

	x = np.array(x)
	y = np.array(y)

	if norm:
		x = x / (dim[ 0 ])
		y = y / (dim[ 1 ])

		if type(norm) in (float, int):
			norm = [ norm, norm ]

		x *= norm[ 0 ]
		y *= norm[ 1 ]

	if s_norm:
		x = x * 2. - 1.
		y = y * 2. - 1.

		if type(s_norm) in (float, int):
			s_norm = [ s_norm, s_norm ]

		x *= s_norm[ 0 ]
		y *= s_norm[ 1 ]

	f = x

	if func is str:
		f = eval(func)
	if func is list:
		f = func

	g[ :, : ] = 1. - f
	g2 = np.rot90(g)
	g *= g2
	g = np.greater_equal(g, 0.2)

	if gray:
		plt.gray()

	if return_only_x is not None:
		return f
	else:
		return g


# ----File and folder processing------------------------------------------------------------------------

class FileManager:
	"""Manage importing, exporting, parsing and creating
	files and folders."""

	def __init__(self, query=None, folder=None, file=None, ext_filter=".jpg", verbose=0):
		self.root = None
		self.folder = folder
		self.file = file
		self.ext_filter = ext_filter
		self.file_dict = dict()
		self.idx = 0
		self.verbose = verbose
		query = str(query)
		if (query or folder or file) is not None:
			it_is_dir = Path(query).is_dir()
			it_is_file = Path(query).is_file()
			if it_is_dir:
				if self.verbose:
					print("FOLDER:", "\t", it_is_dir, "\t", query)
				self.folder = Path(query).absolute().as_posix()
			if it_is_file:
				if self.verbose:
					print("FILE:", "\t", it_is_file, "\t", query)
				self.file = query
		if self.file:
			self.file_folder = Path(self.file).absolute().as_posix()
			self.text_iter(self.file_folder)
		elif self.folder:
			self.root = self.root_path(Path(self.folder).absolute()).as_posix()
			self.get_files()
			if self.verbose:
				self.print_folder_info()

	def __call__(self, *args, **kwargs):
		for k, v in self.file_dict.items():
			print(f'{k}:  \t{v}')

	def make_folder(self, folder=None):
		if not folder:
			folder = self.folder
		if not os.path.exists(folder):
			os.makedirs(folder)
			print("Created Directory:", folder)

	# else:
	# 	print("Directory already existed:", folder)

	def move_file(self, file, new_dir, new_name=None):
		self.make_folder(Path(file).parent.joinpath(new_dir))
		colored = ColorizeText()
		name = Path(file).name
		if new_name is not None:
			name = new_name
		path = Path(file).parent.joinpath(new_dir, name).as_posix().__str__()
		colored.fore = 'light red'
		print_boxed(f'Moving file: {path}')
		file = Path(file).as_posix()
		Path.rename(Path(file), Path(path))
		colored.reset_all()

	def delete_folder_content(self, folder_path=None, ask=True):
		colored = ColorizeText()
		if folder_path is None:
			folder_path = self.folder
		if Path(folder_path).is_dir() is False:
			self.make_folder(folder_path)
		erase = False
		if ask:
			answer = input("Sure?: (y/n)")
			if answer == "y":
				erase = True
		else:
			erase = True
		self.get_folder_files(folder_path)
		if not self.file_dict:
			print("DELETE aborted...")
		elif erase and folder_path:
			colored.fore = "red"
			print_boxed(f'DELETING CONTENT IN FOLDER: "{folder_path}"')
			colored.reset_all()
			time.sleep(2)
			colored.fore = "blue"
			sleep_counter()
			colored.reset_all()
			[ f.unlink() for f in Path(folder_path).glob("*") if f.is_file() ]
			colored.fore = "red"
			print_boxed("FOLDER CONTENT DELETED!")
			colored.reset_all()
			time.sleep(2)

	def get_folder_files(self, folder=None, ext_filter=None):
		from os import listdir
		from os.path import isfile, join

		if folder is None:
			folder = self.folder
		if ext_filter is None:
			ext_filter = self.ext_filter

		files = [ f for f in listdir(folder) if isfile(join(folder, f)) ]
		if files:
			if not ext_filter:
				self.make_files_dict(files)
			else:
				g = [ ]
				for f in files:
					if ext_filter in f:
						g.append(f)

				self.make_files_dict(g)
		else:
			self.file_dict = {}
			print(f'FOLDER contains no files! {folder}')

	def make_files_dict(self, files=None):
		if not files:
			if isinstance(self.file, (list, tuple)):
				files = self.file
			else:
				files = (self.file)
		# self.file_dict = {e:i for e, i in enumerate(sorted(files))}
		self.file_dict = {e: i for e, i in enumerate(files)}

	@property
	def next_file(self):
		self.idx = (self.idx + 1) % len(self.file_dict.keys())
		f = self.file_dict[ self.idx ]
		return f

	@property
	def previous_file(self):
		self.idx = (self.idx - 1) % len(self.file_dict.keys())
		f = self.file_dict[ self.idx ]
		return f

	@property
	def files(self):
		if not self.file_dict:
			if self.folder:
				self.get_folder_files()
			if self.file:
				self.file_dict = self.text_iter(self.file_folder)
		return self.file_dict

	@property
	def files_full_path(self):
		self.file_dict = {k: Path(self.folder).absolute().joinpath(v).as_posix() for k, v in self.files.items()}
		return self.file_dict

	def files_with_path(self, path):
		self.file_dict = {k: f'{path}{v}' for k, v in self.files.items()}
		return self.file_dict

	def get_file(self, idx=None, offset=0):
		if idx is None:
			if not self.file_dict:
				self.get_folder_files()
			self.idx = self.idx + offset
			return self.next_file
		if isinstance(idx, int):
			return self.file_dict[ idx ]
		if isinstance(idx, (tuple, list)):
			return [ self.file_dict[ i ] for i in idx ]

	def get_files(self, folder=None, ext_filter=None):
		if folder is None:
			folder = self.folder
		if ext_filter is None:
			ext_filter = self.ext_filter

		self.get_folder_files(folder, ext_filter)

	def print_files(self):
		for k, v in self.file_dict.items():
			print(f'{k}:  \t{v}')
		return list(self.file_dict.values())

	def current_folder(self):
		p = Path(".").absolute()
		return (p)

	def subdirectories(self, backwards=1):
		p = Path(".").absolute()
		pp = self.root_path(p)
		c = Path(pp).parents[ backwards ]
		return c

	def peer_directories(self):
		p = Path("./..")
		peer = [ x.name for x in p.iterdir() if x.is_dir() ]
		return peer

	def root_path(self, full_path):
		s = "/"
		if isinstance(full_path, str):
			full_path = Path(full_path)
		p = [ *full_path.parts ][ 1: ]
		for item in p:
			if " " in item:
				item = "'" + item + "'"
			s = s + item + "/"
		self.root = s
		return Path(s).absolute()

	def search_dir(self, path, q):
		s = sorted(Path(path).glob(f'**/{q}'))
		return (self.root_path(s[ 0 ]))

	def text_iter(self, path):
		t = TextFileIterator(path)
		return t.dict

	@files_full_path.setter
	def files_full_path(self, value):
		self._files_full_path = value

	def print_folder_info(self):
		print_boxed(f'Folder {self.folder} contains {len(self.file_dict)} files')


class TextFileIterator:

	def __init__(self, path=None):
		self.path = ""
		self.file_dict = dict()
		if path:
			self.path = path
			self.populate_dict()

	def __call__(self, ind, *args, **kwargs):
		return self.file_dict[ ind ]

	@property
	def dict(self):
		return self.file_dict

	def add_to_dict(self, item):
		idx = len(self.file_dict.keys())
		self.file_dict[ idx + 1 ] = item

	def populate_dict(self):
		# self.file_dict = file_to_dict(self.path)
		i = 0
		with open(self.path) as f1:
			lines = f1.readlines()
			for line in lines:
				a = line.strip()
				if a:
					# if a != "" and a.startswith(("//", "\n")) is False:
					self.file_dict[ i ] = a
					i += 1


class NextFileNumber:
	"""Input a folder and a file name and this will
	return next file with added index 1. It can also
	return temp file for the file."""

	def __init__(self, out_path, name_template, additive=1):
		self.out_path = out_path
		self.name_template = name_template
		self.additive = additive
		self.next_file = None
		self.next_file_path = None
		self.temp_file = None
		self.temp_file_path = None

		self.continue_file_numbering()
		self.make_temp_file()

		self.get = self.next_file_path
		self.temp = self.temp_file_path

	def continue_file_numbering(self, out_path=None, name_template=None, additive=0):
		if not out_path:
			out_path = self.out_path
		if not name_template:
			name_template = self.name_template
		if not additive:
			additive = self.additive
		paths, index = search_path_for_file(out_path, name_template)
		out_file_type = name_template.split(".")[ 1 ]
		self.next_file = name_template.replace(f'.{out_file_type}', f'_{int(index) + additive}.{out_file_type}')
		self.next_file_path = self.out_path + self.next_file

	def make_temp_file(self):
		self.temp_file = self.name_template.split(".")[ 0 ] + "_temp." + self.name_template.split(".")[ 1 ]
		self.temp_file_path = self.out_path + self.temp_file


class ImageProcess:
	"""
	img_path = r'D:\CNN_images\Markku_SOURCES\Markku_conv44.jpg'
	dest_path = r'D:\CNN_images\Markku_SOURCES'
	dest_shape = (4724, 4724)
	maintain_ratio = (0, 0)
	postfix = '_resized'
	resampler = 6
	img_proc = ImageProcess(img_path, dest_path, dest_shape, maintain_ratio, postfix, resampler)
	"""

	def __init__(self, path=None, dest_path=None, dest_shape=(4724, 4724), maintain_ratio=(0, 0), postfix="",
			resampler=6):
		self.verbose = None
		self.path = path
		self.dest_path = dest_path
		self.dest_shape = dest_shape
		self.maintain_ratio = maintain_ratio
		self.postfix = postfix
		self.dest_name_postfix = None
		self.dest_path_postfix = None
		self.resample_methods = {
				1: Image.NEAREST,
				2: Image.BOX,
				3: Image.BILINEAR,
				4: Image.HAMMING,
				5: Image.BICUBIC,
				6: Image.LANCZOS}
		self.resampler = resampler

		if self.path:
			self.img = self.load_image(self.path)

		self.is_in_folder = None
		self.is_same_res = None

		if self.dest_path:
			self.in_folder(self.path, self.dest_path, self.postfix)
		if self.path and (self.dest_shape or self.maintain_ratio):
			self.compare_resolution(self.path, self.dest_shape)
		if self.is_same_res is False:
			self.img = self.resize_image(self.img, self.dest_shape, self.maintain_ratio)
		if self.is_in_folder is False:
			self.save_image(self.img, self.dest_path_postfix)

	def load_image(self, path):
		img = Image.open(path)
		return img

	def load_image_to_array(self, path, normalize=0, rotate=0):
		img = Image.open(path)
		if normalize:
			img_arr = np.array(img, dtype=np.float32) / 255.
		else:
			img_arr = np.array(img)
		if rotate:
			img_arr = np.rot90(img_arr, rotate)
		return img_arr

	def get_dim(self, path, verbose=None, rotate=0):
		arr = self.load_image_to_array(path, rotate=rotate)
		if verbose is not None:
			print("Dim:", arr.shape, "\t", Path(path).name)
		return arr.shape[ 0:2 ]

	def enhance_image(self, img, contrast=1., brightness=1., sharpness=1., color=1.):
		if contrast != 1.:
			img = ImageEnhance.Contrast(img).enhance(contrast)
		if brightness != 1.:
			img = ImageEnhance.Brightness(img).enhance(brightness)
		if sharpness != 1.:
			img = ImageEnhance.Sharpness(img).enhance(sharpness)
		if color != 1.:
			img = ImageEnhance.Color(img).enhance(color)
		return img

	def remove_alpha(self, path):
		img = self.load_image(path)
		img = img.convert("RGB")
		return img

	def scale_image(self, img, scale=1., resampler=None):
		if resampler is None:
			resampler = self.resampler
		img = ImageOps.scale(img, scale, self.resample_methods[ resampler ])
		return img

	def pad_image(self, img, size, padding=(0.5, 0.5), resampler=None):
		if resampler is None:
			resampler = self.resampler
		img = ImageOps.pad(img, size, self.resample_methods[ resampler ], centering=padding)
		return img

	def resize_image(self, img, resize=(0, 0), contain=(0, 0), pad=(0., 0.), resampler=None, centering=(0.5, 0.5),
			bleed=0., pad_color=(0, 0, 0)):
		if resampler is None:
			resampler = self.resampler
		if isinstance(img, str):
			img = self.load_image(path=img)
		if sum(resize):
			img = ImageOps.fit(img, resize, method=self.resample_methods[ resampler ], bleed=bleed,
			                   centering=centering)
		if sum(contain):
			img = ImageOps.contain(img, contain, method=self.resample_methods[ resampler ])
		if sum(pad):
			img = ImageOps.pad(img, pad, method=self.resample_methods[ resampler ], color=pad_color,
			                   centering=centering)
		return img

	def resize_and_save(self, img_path, dest_dim, centering=(0.5, 0.5), ext=None):
		out_path = ""
		if ext is None:
			out_path = img_path
		else:
			stem = Path(img_path).stem.__str__()
			suffix = Path(img_path).suffix.__str__()
			if "." in ext:
				suffix = ""
			out_path = Path(Path(img_path).parent).joinpath(Path(stem + ext + suffix)).as_posix()
		# print(out_path)
		img = self.load_image(img_path)
		img = self.resize_image(img, resize=dest_dim, centering=centering)
		self.overwrite(img, out_path)
		return out_path

	def resize_multi_sharp(self, img_path, target_dim, out_path=None, name=None, ext=None, sharp_depth=0.6,
			blur_depth=0.1, iter_amt=2, centering=(0.5, 0.5), bleed=0.):
		if out_path is None:
			out_path = Path(img_path).parent
		if name is None:
			name = Path(img_path).name
		if ext is not None:
			stem = Path(img_path).stem.__str__()
			suffix = Path(img_path).suffix.__str__()
			if "." in ext:
				suffix = ""
			name = Path(stem + ext + suffix).as_posix()
		out_path = Path(out_path).joinpath(name).as_posix().__str__()
		print(out_path)
		img = self.load_image(img_path)
		dim = np.array(target_dim)
		amt = iter_amt
		for i in range(amt):
			sharp = (i / (amt - 1)) * sharp_depth + (2. - sharp_depth)
			# sharp = 2.
			blur = (i / (amt - 1)) * blur_depth + (1. - blur_depth)
			# print("SHARP:", sharp, "BLUR:", blur)
			# img = img_op.enhance_image(img, sharpness=sharp)
			img = self.enhance_image(img, sharpness=blur)
			img = self.resize_image(img, resize=np.array((dim / (amt - i)), dtype=np.int32), resampler=6,
			                        centering=centering, bleed=bleed)
			img = self.enhance_image(img, sharpness=sharp)
		self.save_image(img, out_path)
		return out_path

	def save_with_suffix(self, img_path, ext=None):
		if ext is None:
			out_path = img_path
		else:
			stem = Path(img_path).stem.__str__()
			suffix = Path(img_path).suffix.__str__()
			if "." in ext:
				suffix = ""
			out_path = Path(Path(img_path).parent).joinpath(Path(stem + ext + suffix)).as_posix()
		img = self.load_image(img_path)
		self.overwrite(img, out_path)
		return out_path

	def save_image(self, img, path=None, verbose=None):
		if verbose is not None:
			verbose = self.verbose
		if self.verbose is not None:
			print("Saved image:\t\t\t", path)
		if path is not None:
			img.save(path, quality=95)
		else:
			img.save(self.path, quality=95)

	def img_to_numpy32f(self, img1_path=None, img2_path=None):
		""" Takes two image paths, loads them, and returns them as 32f numpy arrays."""
		if img1_path is None:
			img1_path = self.path

		im1 = self.load_image(img1_path)
		im1_arr = np.array(im1, dtype=np.float32) / 255.

		if img2_path:
			im2 = self.load_image(img2_path)
			im2_arr = np.array(im2, dtype=np.float32) / 255.

			im1_shape = np.array(im1_arr).shape[ 0:2 ]
			im2_shape = np.array(im2_arr).shape[ 0:2 ]

			if im1_shape == im2_shape:
				pass
			elif im1_shape > im2_shape:
				im2 = self.resize_image(im2, resize=im1_shape)
				im2_arr = np.array(im2, dtype=np.float32) / 255.
			else:
				im1 = self.resize_image(im1, resize=im2_shape)
				im1_arr = np.array(im1, dtype=np.float32) / 255.

			return im1_arr, im2_arr
		else:
			return im1_arr

	def blend(self, path_1, path_2, cross_fade):
		im1 = self.load_image(path_1)
		im2 = self.load_image(path_2)
		if im1.size != im2.size:
			im2 = self.resize_image(im2, im1.size)
		return Image.blend(im1, im2, cross_fade)

	def resize_check_load(self, path_1, path_2):
		im1 = self.load_image(path_1)
		im2 = self.load_image(path_2)
		if im1.size != im2.size:
			im2 = self.resize_image(im2, im1.size)
		return im1, im2

	def equalize(self, img):
		return ImageOps.equalize(img)

	def rgb2hsv(self, img):
		return img.convert('HSV')

	def hsv2rgb(self, img):
		return img.convert('RGB')

	def swap_hsv(self, path_1, path_2, fades=(0.5, 0.5, 0.5)):
		im1, im2 = self.resize_check_load(path_1, path_2)
		im1, im2 = self.rgb2hsv(im1), self.rgb2hsv(im2)
		h1, s1, v1 = im1.split()
		h2, s2, v2 = im2.split()
		h, s, v = Image.blend(h1, h2, fades[ 0 ]), Image.blend(s1, s2, fades[ 1 ]), Image.blend(v1, v2, fades[ 2 ])
		im = Image.merge('HSV', (h, s, v))
		return self.hsv2rgb(im)

	def overwrite(self, img, img_path):
		img.save(img_path)
		if self.verbose is not None:
			print("Saved image:\t\t\t", img_path)

	def load_image_from_array(self, img):
		img = np.array(img * 255., dtype=np.uint8)
		img = Image.fromarray(img)
		return img

	def save_image_from_array(self, arr, path):
		arr = np.array(arr * 255., dtype=np.uint8)
		Image.fromarray(arr).save(path)
		if self.verbose is not None:
			print("Saved array image:\t\t", path)

	def with_postfix(self, src, postfix=None):
		if postfix is None:
			postfix = self.postfix
		self.dest_name_postfix = Path(src).stem.__str__() + postfix + Path(src).suffix.__str__()
		self.dest_path_postfix = Path(Path(src).parent).joinpath(self.dest_name_postfix).as_posix()

	def in_folder(self, src, dest, postfix=None):
		if postfix is None:
			postfix = self.postfix

		self.with_postfix(src, postfix)
		print(f'\nChecking folder for {self.dest_name_postfix}...')
		print(self.dest_path_postfix)
		if os.path.exists(self.dest_path_postfix) is False:
			print(f'No resized version of "{Path(src).stem}" in destination folder!!')
			# self.check_and_resize(src, dest=if_resized, dest_shape=dest_shape)
			# print(f'New path: {if_resized}')
			self.is_in_folder = False
		else:
			print(f'"{Path(self.dest_path_postfix).name}" already in: {dest}')
			self.is_in_folder = True

	def compare_resolution(self, src, dest_shape=None):
		if self.img is None:
			img = self.load_image(src)
		else:
			img = self.img
		if dest_shape is None:
			dest_shape = self.dest_shape

		src_shape = np.array(img).shape[ 0:2 ]

		if src_shape != dest_shape:
			print(f'Resolutions dissimilar: {src_shape} != {dest_shape}')
			self.is_same_res = False
		else:
			self.is_same_res = True


class ImageCollage:

	def __init__(self, list_of_images, size, col_row, path=None, name="Collage.jpg", quality=95, resampler=6, border=0,
			mirror=(0, 0), flip=(0, 0), rotate=0, verbose=1):
		self.path = path
		if path is None:
			self.path = "."
		self.name = Path(self.path).joinpath(name).as_posix().__str__()
		self.size = size
		self.col_row = col_row

		max_arrange = max(col_row)
		max_size = max(size)
		min_size = int(max_size / max_arrange)
		self.verbose = verbose

		self.quality = quality
		self.flip = flip
		self.mirror = mirror
		self.border = border
		self.rotate = rotate

		resample_methods = {
				1: Image.NEAREST,
				2: Image.BOX,
				3: Image.BILINEAR,
				4: Image.HAMMING,
				5: Image.BICUBIC,
				6: Image.LANCZOS}

		self.resampler = resample_methods[ resampler ]

		# if self.size[0] > self.size[1]:
		# 	self.size = max_size, min_size
		# 	self.col_row = self.col_row[1], self.col_row[0]
		# else:
		# 	# self.size = min_size, max_size
		# 	self.size = size
		# 	self.col_row = col_row

		self.create_collage(list_of_images, self.size, self.col_row)

	@bordered
	def create_collage(self, list_of_images, size, col_row):
		width, height = size
		cols, rows = col_row

		thumbnail_width = width // cols
		thumbnail_height = height // rows
		size = thumbnail_width, thumbnail_height
		new_im = Image.new('RGB', (width, height), 'black')
		# new_im = Image.new('RGB', (width, height), 'white')
		ims = [ ]
		for p in list_of_images:
			im = Image.open(p)
			# im.thumbnail(size, resample=Image.LANCZOS)
			# im = ImageOps.fit(im, (size[0]-self.border, size[1]-self.border), Image.LANCZOS)
			# im = ImageOps.contain(im, size, method=Image.BICUBIC)
			im = ImageOps.contain(im, size, method=Image.BILINEAR)
			if self.border:
				im = ImageOps.expand(im, self.border)
			ims.append(im)
		i = 0
		x = 0
		y = 0
		for col in range(cols):
			for row in range(rows):
				if self.mirror[ 2 ] == 2:
					if self.mirror[ 0 ]:
						if ((i % 8) - 4) >= 0:
							ims[ i ] = ImageOps.mirror(ims[ i ])
					if self.mirror[ 1 ]:
						if i % 2 == 0:
							ims[ i ] = ImageOps.mirror(ims[ i ])
				if self.flip[ 0 ]:
					if i % 2 == 0:
						ims[ i ] = ImageOps.flip(ims[ i ])
				if self.flip[ 1 ]:
					if i % 2 == 1:
						ims[ i ] = ImageOps.flip(ims[ i ])
				if self.mirror[ 2 ] == 1:
					ims[ i ] = ImageOps.mirror(ims[ i ])
				if self.rotate:
					ims[ i ] = Image.Image.rotate(ims[ i ], 90 * self.rotate, resample=3)
				# print(i, x, y)
				if self.verbose:
					print(f'{Path(list_of_images[ i ]).name:50} >> [Col: {col}][Row: {row}]: {x} {y}')
				new_im.paste(ims[ i ], (x, y))
				i += 1
				y += thumbnail_height
			x += thumbnail_width
			y = 0

		new_im.save(self.name, quality=self.quality)
		print("\nImage collage saved:", self.name)


def log_time(prefix="Run on: "):
	return f'{prefix}{datetime.today().strftime("%d-%m-%Y - %H:%M:%S"):^21}'


def log_to_file(*args, **kwargs):
	verbose = kwargs.get('verbose')
	path = kwargs.get("path")
	if path is None:
		path = Path(".")
	idx = kwargs.get("idx")
	if idx is None:
		idx = ""
	else:
		idx = f'{idx}: '
	name = kwargs.get("name")
	if name is None:
		name = "_temp"
	mode = kwargs.get("mode")
	if mode is None:
		mode = "w"
	file = Path(path).joinpath(f'log_{name}.txt').as_posix()
	type_string = ""
	a = [ ]
	c = [ ]
	f = open(file, mode)
	for i in args:
		if isinstance(i, (int, float)):
			c.append(i)
		elif isinstance(i, (list, tuple)):
			a = i
			type_string = "list"
			b = f'{idx}{a}\n'
			if verbose:
				print(f'[Logged {type_string} to {file}]')
			f.write(b)
		elif isinstance(i, dict):
			a = i
			type_string = "dictionary"
			b = f'{idx}{a}\n'
			if verbose:
				print(f'[Logged {type_string} to {file}]')
			f.write(b)
		elif isinstance(i, str):
			a = i
			type_string = "string"
			b = f'{idx}{a}\n'
			if verbose:
				print(f'[Logged {type_string} to {file}]')
			f.write(b)
	if c:
		b = f'{idx}{c}\n'
		type_string = "args as list"
		if verbose:
			print(f'[Logged {type_string} to {file}]')
		f.write(b)
	f.close()


def text_to_file(filename, txt_string, mode="w"):
	# f = open(filename, mode)
	# f.write(txt_string)
	# f.close()
	with open(filename, mode) as f:
		f.write(f'{txt_string}\n')


def list_to_file(my_list, filename):
	with open(filename, 'w') as f:
		for item in my_list:
			f.write("%s\n" % item)


def file_to_dict(filename, verbose=0):
	file_data = dict()
	i = 0
	with open(filename) as f1:
		lines = f1.readlines()
		for line in lines:
			a = line.strip()
			if a != "" and a.startswith(("//", "\n")) is False:
				file_data[ i ] = eval(a)
				i += 1

	if verbose:
		print(file_data)
	return file_data


def import_file(filepath):
	with open(filepath, 'r') as file:
		query = file.read()
	return query


def file_to_string(filename, verbose=0):
	file_data = ""
	with open(filename) as f1:
		lines = f1.readlines()
		print(lines)
		for line in lines:
			a = line.strip()
			if a != "" and a.startswith(("//", "\n")) is False:
				file_data += a + "\n"
	if verbose:
		print(file_data)
	return file_data


def search_path_for_file(path, s):
	"""Return the full path of the files matching `s` in `path`
	and the index of the latest entry."""
	l = [ ]
	p = [ ]
	n = [ ]
	if "." in s:
		s = s.split(".")[ 0 ]
	for root, dirs, files in os.walk(path):
		for basename in files:
			if s in basename:
				filename = os.path.join(root, basename)
				file_mod = filename.split(".")[ 0 ].split("_")
				for int_test in file_mod:
					try:
						x = int(int_test)
						n.append(x)
					except Exception:
						pass
				p.append(filename)
				l.append(basename)
		# print("Found", len(l))
		if len(n) >= 1:
			i = max(n)
			# print(f'Latest index is {i}')
			return p, i
		else:
			return s, 0


# DELETE?
def search_file_index(s, end="."):
	"""Cut the index between comma and any kind of dash."""
	before_index = ("-", "_")
	s = s.split(end)[ 0 ][ ::-1 ]
	for i in before_index:
		if i in s:
			s = s.split(i)[ 0 ]
	return s


# ----String processing------------------------------------------------------------------------

def cut(in_string, start, end):
	start = str(start)
	end = str(end)
	strip = ""
	for line in in_string.splitlines():
		if start:
			m = line.find(start)
			if m >= 0:
				strip = in_string.split(start)[ 1 ]
			if end:
				m = strip.find(end)
				if m >= 0:
					strip = strip.split(end)[ 0 ]
		else:
			m = line.find(end)
			if m >= 0:
				strip = in_string.split(end)[ 0 ]
	return strip.strip()


def select(in_string, start):
	strip = ""
	for line in in_string.splitlines():
		m = line.find(start)
		if m >= 0:
			strip = line
	return strip.strip()


def include(in_string, start, end, extra_line=0, verbose=0):
	strip = ""
	gate = 0
	for i, line in enumerate(in_string.splitlines()):
		m = line.find(start)
		n = line.find(end)
		if verbose:
			print(i, line, m, n)
		if m >= 0:
			gate = 1
		if gate:
			strip += line.strip() + "\n"
		if n >= 0 and gate == 1:
			if extra_line:
				strip += in_string.splitlines()[ i + 1 ].strip() + "\n"
			break
	return strip


def list_to_string(s):
	return f' '.join(map(str, s))


def strip_string(string):
	strip = ""
	lines = string.splitlines()
	for line in lines:
		a = line.strip()
		if a != "" and a.startswith(("//", "\n")) is False:
			strip += (a + "\n")
	return strip


def merge(dict1, dict2):
	return dict1.update(dict2)


def merge_2(dict1, dict2):
	res = {**dict1, **dict2}
	return res


class Parse:
	""" Parse input file based on searchquery and endquery strings """

	def __init__(self, output_file="", input_file="", input_file_string=""):
		self.output_file = output_file
		self.input_file = input_file
		self.input_file_string = input_file_string

		if not self.output_file:
			self.output_file = "_" + self.input_file

	def clear(self):
		with open(self.output_file, 'w') as f2:
			f2.write("")

	def cut_with_starts(self, searchquery, endquery, mode='a'):
		with open(self.input_file) as f1:
			with open(self.output_file, mode) as f2:
				lines = f1.readlines()
				for i, line in enumerate(lines):
					if line.startswith(searchquery):
						f2.write(lines[ i ])
						while lines[ i ].strip().startswith(endquery) is not True:
							f2.write(lines[ i + 1 ])
							i += 1

	def cut_with_starts_string(self, searchquery, endquery, to_file=0, mode='a'):
		strip = ""
		with open(self.output_file, mode) as f2:
			lines = self.input_file_string.splitlines()
			for i, line in enumerate(lines):
				if line.startswith(searchquery):
					strip += (str(i) + " " + lines[ i ] + "\n")
					if to_file:
						f2.write(lines[ i ])

		self.input_file_string = strip
		return strip

	def cut_with_chars(self, searchquery, endquery, mode='a'):
		start = 0
		with open(self.input_file) as f1:
			with open(self.output_file, mode) as f2:
				lines = f1.readlines()
				for i, line in enumerate(lines):
					for c in line:
						if searchquery in c:
							start = 1
						if endquery is c:
							start = 0
							f2.write(lines[ i ] + "\n")

					if start:
						f2.write(lines[ i ])

	def cut_with_words_end(self, searchquery, endquery, to_file=0, mode='a'):
		start = 0
		with open(self.input_file) as f1:
			with open(self.output_file, mode) as f2:
				lines = f1.readlines()
				for i, line in enumerate(lines):
					if line.strip().startswith(searchquery):
						# print(word)
						start = 1

					if start:
						if to_file:
							f2.write(lines[ i ])

					if line.strip().endswith(endquery):
						# print(word)
						start = 0

	def cut_with_words_end_string(self, searchquery, endquery, to_file=0, mode='a'):
		start = 0
		strip = ""
		with open(self.output_file, mode) as f2:
			lines = self.input_file_string.splitlines()
			for i, line in enumerate(lines):
				if line.strip().startswith(searchquery):
					# print(word)
					start = 1

				if start:
					strip += (lines[ i ] + "\n")
					if to_file:
						f2.write(lines[ i ])

				if line.strip().endswith(endquery):
					# print(word)
					start = 0

		self.input_file_string = strip
		return strip

	def cut_with_words_file(self, searchquery, endquery, to_file=0, mode='a'):
		start = 0
		strip = ""
		with open(self.input_file) as f1:
			with open(self.output_file, mode) as f2:
				lines = f1.readlines()
				for i, line in enumerate(lines):
					for word in line.split():
						if searchquery in word:
							# print(word)
							start = 1
						if endquery in word and start:
							# print(word)
							start = 0
					# f2.write(lines[i]+"\n")
					if start:
						strip += (lines[ i ] + "\n")
						if to_file:
							f2.write(lines[ i ])

		self.input_file_string = strip
		return strip

	def cut_with_words_string(self, searchquery, endquery, to_file=0, mode='a'):
		start = 0
		strip = ""
		with open(self.output_file, mode) as f2:
			lines = self.input_file_string.splitlines()
			for i, line in enumerate(lines):
				for word in line.split():
					if searchquery in word:
						start = 1

				if start:
					strip += (str(i) + " " + lines[ i ] + "\n")

					if endquery in word and start:
						start = 0
					# f2.write(lines[i]+"\n")
					if to_file:
						f2.write(lines[ i ])

		self.input_file_string = strip
		return strip

	def cut_before_after(self, start, end):
		strip = ""
		for line in self.input_file_string.splitlines():
			m = line.find(start)
			if m >= 0:
				strip = self.input_file_string.split(start)[ 1 ]

			m = strip.find(end)
			if m >= 0:
				strip = strip.split(end)[ 0 ]

		self.input_file_string = strip
		return strip

	def strip_file(self, to_file=0, mode='a'):
		strip = ""
		with open(self.input_file) as f1:
			with open(self.output_file, mode) as f2:
				lines = f1.readlines()
				for line in lines:
					a = line.strip()
					if a != "" and a.startswith(("//", "\n")) is False:
						# print(a)
						if to_file:
							f2.write(a + "\n")
						strip += (a + "\n")

		self.input_file = strip
		return strip

	def strip_string(self, to_file=0, mode='a'):
		strip = ""
		with open(self.output_file, mode) as f2:
			lines = self.input_file_string.splitlines()
			for line in lines:
				a = line.strip()
				if a != "" and a.startswith(("//", "\n")) is False:
					strip += (a + "\n")

					if to_file:
						f2.write(a + "\n")

		self.input_file_string = strip
		return strip

	def string_to_file(self, string, mode='a'):
		with open(self.output_file, mode) as f2:
			lines = string.splitlines()
			for line in lines:
				a = line.strip()
				f2.write(a + "\n")

	def check_if_line(self, compare_file=None):
		with open(self.input_file) as f1:
			if compare_file:
				with open(compare_file) as f2:
					lines1 = f1.readlines()
					lines2 = f2.readlines()
					for i1, line1 in enumerate(lines1):
						for i2, line2 in enumerate(lines2):
							if line1.strip() in line2:
								print(line1.strip(), "found in", compare_file)


# ----Math processing------------------------------------------------------------------------


class Fibonacci:

	def __init__(self, n=10):
		self.n = n

	def fibonacci(self, n):
		curr, nxt = 0, 1
		for _ in range(n):
			curr, nxt = nxt, curr + nxt
		return curr

	def as_list(self, n=None):
		l = [ ]
		if not n:
			n = self.n
		for i in range(n):
			# print(f'{i}:  {self.fibonacci(i)}')
			l.append(self.fibonacci(i))
		# print(l)
		return l

	@property
	def golden_ratio(self):
		return 1.618033988749


class PrimeNumbers:

	def __init__(self, n=None):
		self.n = n
		self.prime_list = None
		if n is not None:
			self.prime_list = self.amt(n)

	def is_prime(self, num):
		if num > 1:
			# check for factors
			for i in range(2, num):
				if (num % i) == 0:
					break
			else:
				return num

	def up_to(self, max_int):
		prime_list = [ ]
		i = 0
		while i < max_int:
			n = self.is_prime(i)
			if n > 0:
				prime_list.append(n)
			i += 1
		return prime_list

	def amt(self, max_int):
		prime_list = [ ]
		i = 0
		while len(prime_list) < max_int:
			n = self.is_prime(i)
			if n > 0:
				prime_list.append(n)
			i += 1
		return prime_list


class RecursiveFibonacci:
	from functools import lru_cache

	def __init__(self, n=32):
		self.n = n

	@lru_cache(maxsize=32)
	def recursive_fibonacci(self, n):
		if n in [ 0, 1 ]:
			return n
		return self.recursive_fibonacci(n - 1) + self.recursive_fibonacci(n - 2)

	def iterate(self, n=None):
		if not n:
			n = self.n
		return [ self.recursive_fibonacci(i) for i in range(n) ]
