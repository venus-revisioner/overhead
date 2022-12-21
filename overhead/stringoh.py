import os
import re

from overhead.dictoh import sort_dictionary


def read_txt_file(file_name):
	with open(file_name, 'r') as file:
		return file.read()


def save_txt_file(file_name, s):
	with open(file_name, 'w') as file:
		file.write(s)


def get_txt_files_from_dir(dir_path):
	return [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f.endswith(".txt")]


def get_paragraphs_from_text(text):
	return text.split("\n\n")


def get_paragraphs_from_txt_file(file_name):
	text_file_string = read_txt_file(file_name)
	return text_file_string.split("\n\n")


def get_paragraphs_from_directory(dir_path):
	text_files = get_txt_files_from_dir(dir_path)
	paragraphs = []
	for file_name in text_files:
		file_path = os.path.join(dir_path, file_name)
		paragraphs.extend(get_paragraphs_from_txt_file(file_path))
	return paragraphs


def remove_line_numbers(s):
	return re.sub(r'\d+\s*', '', s)


def remove_newlines(s):
	return s.replace("\n", " ")


def remove_punctuations(s):
	return re.sub(r'[^\w\s]', '', s)


def remove_stopwords(s):
	import stopwords
	if isinstance(s, str):
		s = tokenize_string(s)
	stop_words = set(stopwords.get_stopwords('english'))
	reduced = [w for w in s if w not in stop_words]
	return " ".join(reduced)


def tokenize_word(s):
	tokens = s.split(' ')
	tokens = [i for i in tokens if i]
	return tokens


def tokenize_string(s):
	return tokenize_word(s)


def tokenize_sentence(s):
	return tokenize_word(s)


def tokenize_paragraph(s):
	return tokenize_sentence(s)


def tokenize_text(s):
	return tokenize_paragraph(s)


def tokenize_file(input_file, output_file):
	text = read_txt_file(input_file)
	tokens = tokenize_string(text)
	save_txt_file(output_file, '\n'.join(tokens))
	return tokens


def get_words(text):
	return re.compile('[a-zA-Z]+').findall(text)


def get_sentences(text):
	return tokenize_sentence(text)


def get_unique_words(text):
	words = get_words(text)
	return set(words)


def remove_numbers(words):
	clean = re.compile('[a-zA-Z]+').findall(words)
	return " ".join(clean)


def remove_empty_words(words):
	return [word for word in words if len(word) > 0]


def get_word_frequencies(words):
	"""
	The get_word_frequencies function takes a list of words and returns a dictionary with the frequency of each word.
	The function is case insensitive, so all words are converted to lowercase before counting.
	:param words: Pass in a list of words to be counted
	:return: A dictionary of words and their frequencies
	"""
	frequencies = {}
	for word in words:
		word = word.lower()

		if word in frequencies:
			frequencies[word] += 1
		else:
			frequencies[word] = 1
	return sort_dictionary(frequencies, 1)


def get_word_frequencies_sorted_list(s):
	s = remove_line_numbers(s)
	s = remove_newlines(s)
	s = sanitize_extra_chars(s)
	# s = remove_punctuations(s)
	# s = remove_stopwords(s)
	s = tokenize_string(s)
	# s = get_unique_words(s)
	s = get_word_frequencies(s)
	return s


def get_substring_occurences(s, substring):
	return [i for i in range(len(s)) if s.startswith(substring, i)]


def sanitize_text(s, remove_chr="#$&\'/_()*+:;<=>[]^`{|}~" + '"'):
	return s.translate({ord(i): "" for i in remove_chr})


def sanitize_extra_chars(s, remove_chr="#$@£$%&\/-_()*+:;<=>[]^{'`|}~!?,." + '"'):
	return s.translate({ord(i): "" for i in remove_chr})


def clean_text(text):
	"""
	The clean_text function takes a string as input and returns a list of words
	that have been cleaned by removing stopwords, punctuations, and numbers.
	:param text: Pass in the text that needs to be cleaned
	:return: A list of words
	"""
	words = remove_punctuations(text)
	words = remove_stopwords(words)
	words = remove_numbers(words)
	return words


def read_file_example(text_file):
	from pprint import pprint
	s = read_txt_file(text_file)
	s = remove_line_numbers(s)
	s = remove_newlines(s)
	s = sanitize_extra_chars(s)
	# s = remove_punctuations(s)
	# s = remove_stopwords(s)
	s = tokenize_string(s)
	# s = get_unique_words(s)
	s = get_word_frequencies(s)
	# print(s)
	# pprint(s)
	return s


def analyze_string(s):
	s = remove_newlines(s)
	s = sanitize_extra_chars(s)
	s = remove_punctuations(s)
	s = remove_stopwords(s)
	s = tokenize_string(s)
	s = get_word_frequencies(s)
	return s


def characters_in_string(s):
	s = remove_newlines(s)
	s = remove_punctuations(s)
	s = sanitize_text(s)
	s = [c for c in s]
	s = "".join(s)
	return s

# _TEXT_FILE = "/Volumes/GoogleDrive/Other computers/WIN10/PycharmProjects/OpenAI/AI_me.txt"
# example_1(_TEXT_FILE)
# s = get_word_frequencies_sorted_list(read_txt_file(_TEXT_FILE))
# pprint(s)
