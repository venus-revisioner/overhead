# coding=utf-8

def sort_dictionary(sort_dict, keyword):
	return sorted(sort_dict.items(), key=lambda x: x[keyword], reverse=True)
