# coding=utf-8
from json import load, decoder, dump


class JSONhelper:
	def __init__(self):
		self.json_dict = None
		self.decoder = decoder.JSONDecoder()

	def decode(self, s):
		return self.decoder.decode(s)

	def load_file(self, json_file):
		try:
			with open(json_file) as file:
				self.json_dict = load(file)
			return self.json_dict
		except Exception as e:
			print(e)
			print("JSON file not found...")

	def save_file(self, save_file, json_dict, mode='w'):
		with open(save_file, mode) as file:
			dump(json_dict, file, indent=2)
