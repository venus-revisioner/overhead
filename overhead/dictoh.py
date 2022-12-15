# coding=utf-8
# from overhead import *
from overhead.toolboxoh import FileManager


def sort_dictionary(sort_dict, keyword):
	return sorted(sort_dict.items(), key=lambda x: x[keyword], reverse=True)
