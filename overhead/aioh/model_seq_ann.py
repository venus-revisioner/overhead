import keras
import numpy as np
from keras.layers.core import Dense
from keras.models import Sequential, load_model, Model
from keras.preprocessing.text import Tokenizer
from PIL import Image
from torchvision.utils import save_image



def load_text(path):
	with open(path, 'r') as f:
		text = f.read()
	return text

def load_image(path):
	image = Image.open(path)
	image = image.convert('RGB')
	image = np.array(image)
	image = image.transpose(2, 0, 1)
	image = image / 255
	return image

def save_image(image, path):
	image = image * 255
	image = image.transpose(1, 2, 0)
	image = image.astype(np.uint8)
	image = Image.fromarray(image)
	image.save(path)

def save_images(images, path):
	images = images * 255
	images = images.transpose(0, 2, 3, 1)
	images = images.astype(np.uint8)
	for i, image in enumerate(images):
		image = Image.fromarray(image)
		image.save(path + str(i) + ".png")

def load_images(path, num_images):
	images = []
	for i in range(num_images):
		image = load_image(path + str(i) + ".png")
		images.append(image)
	return images

def load_images_from_folder(folder):
	images = []
	for filename in os.listdir(folder):
		img = cv2.imread(os.path.join(folder,filename))
		if img is not None:
			images.append(img)
	return images


def tokenize_text_to_seq(text, num_words=None, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t"", \n',
						 lower=True, split=" ", char_level=False, oov_token=None, document_count=0):
	"""
	:param text: list of strings
	:param filters: string of punctuation to filter out
	:param lower: boolean. Whether to convert the texts to lowercase.
	:param split: str. Separator for word splitting.
	:param char_level: if True, every character will be treated as a token.
	:param oov_token: if given, it will be added to word_index and used to replace out-of-vocabulary words during text_to_sequence calls
	:param num_words: the maximum number of words to keep, based on word frequency. Only the most common num_words-1 words will be kept.
	:param document_count: int. if set to a number >= 1, filter out tokens that were seen in
	:return: tokenizer, word_index, word_counts
	"""
	tokenizer = Tokenizer(filters=filters, lower=lower, split=split, char_level=char_level, oov_token=oov_token, num_words=num_words)
	tokenizer.fit_on_texts(text)
	word_index = tokenizer.word_index
	word_counts = tokenizer.word_counts
	if document_count > 0:
		word_index = {key: value for key, value in word_index.items() if word_counts[key] >= document_count}
	return tokenizer, word_index, word_counts


def tokenize_text(text, filters='!"#$%&()*	+,-./:;<=>?@[\\]^_`{|}~\t"',
				  lower=True, split=" ", char_level=False, oov_token=None, num_words=1024, document_count=0):

	tokenizer = Tokenizer(filters=filters, lower=lower, split=split, char_level=char_level, oov_token=oov_token, num_words=num_words)
	print("Length of text: {} characters".format(len(text)))
	# Take a look at the first 250 characters in text
	# The unique characters in the file
	vocab = sorted(set(text))
	print('{} unique characters'.format(len(vocab)))
	# Process the text
	num_words = len(vocab)
	print("num_words: ", num_words)
	print("Creating tokenizer...")
	# fit the tokenizer on the documents
	print("Fitting tokenizer...")
	tokenizer.fit_on_texts(text)
	print("Tokenizer fitted.")
	# summarize what was learned
	print("Summarizing...")
	word_index = tokenizer.word_index
	print("Word index: ", word_index)
	print("Found %s unique tokens." % len(word_index))
	# integer encode the documents
	print("Encoding...")
	encoded_text = tokenizer.texts_to_sequences(text)
	print("Encoded text: ", encoded_text)
	print("Encoded text length: ", len(encoded_text))
	# pad documents to a max length of 4 words
	print("Padding...")
	max_length = max([len(s.split()) for s in text])
	print("Max length: ", max_length)
	padded_text = keras.preprocessing.sequence.data_utils.pad_sequences(encoded_text, maxlen=max_length, padding='post')
	print("Padded text: ", padded_text)
	print("Padded text length: ", len(padded_text))

	return tokenizer, word_index, padded_text, max_length


def create_model(input_shape, output_shape, num_layers, num_neurons, activation, loss, optimizer, metrics):
	"""
	:param input_shape: shape of input
	:param output_shape: shape of output
	:param num_layers: number of layers
	:param num_neurons: number of neurons in each layer
	:param activation: activation function
	:param loss: loss function
	:param optimizer: optimizer
	:param metrics: metrics
	:return: model
	"""
	model = Sequential()
	model.add(Dense(num_neurons, input_shape=input_shape, activation=activation))
	for i in range(num_layers - 1):
		model.add(Dense(num_neurons, activation=activation))
	model.add(Dense(output_shape, activation=activation))
	model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
	return model


def text_to_matrix(text, word_index, max_length):
	"""
	:param text: list of strings
	:param word_index: word index
	:param max_length: max length of text
	:return: matrix of text
	"""
	encoded_text = []
	for sentence in text:
		encoded_sentence = []
		for word in sentence.split():
			encoded_sentence.append(word_index[word])
		encoded_text.append(encoded_sentence)

	padded_text = keras.preprocessing.sequence.data_utils.pad_sequences(encoded_text, maxlen=max_length, padding='post')
	matrix = np.zeros((len(padded_text), max_length, len(word_index) + 1))
	for i, sentence in enumerate(padded_text):
		for j, word in enumerate(sentence):
			matrix[i, j, word] = 1
	return matrix


	# text_matrix = keras.preprocessing.sequence.data_utils.pad_sequences(sequences, maxlen=max_length, padding='post')
	# return text_matrix
	# print("------------------ Summarizing tokenizer ------------------")
	# print("Tokenizer word index: ", tokenizer.word_index)
	# print("Tokenizer word counts: ", tokenizer.word_counts)
	# print("Tokenizer document count: ", tokenizer.document_count)
	# print("Tokenizer word docs: ", tokenizer.word_docs.items())
	# # integer encode documents
	# print("Encoding documents...")
	# encoded_docs = keras.preprocessing.text.Tokenizer.texts_to_matrix(tokenizer, textc, mode='binary')
	# print(encoded_docs)
	# print("Returning tokenizer and encoded docs as a tuple of numpy arrays.")
	# print("Shape of encoded docs: ", encoded_docs.shape, " and type: ", type(encoded_docs))
	# print("Shape of tokenizer.word_index: ", len(tokenizer.word_index), " and type: ", type(tokenizer.word_index))
	# print("Compress ratio from input:", len(text), "to output", len(encoded_docs), "is", len(text) / len(encoded_docs))
	# return tokenizer, encoded_docs


def decode_sequence(tokenizer, sequence):
	"""
	:param tokenizer: tokenizer used to tokenize the text
	:param sequence: sequence to decode
	:return: decoded sequence
	"""
	word_index = tokenizer.word_index
	index_word = {value: key for key, value in word_index.items()}
	decoded_sequence = []
	for i in sequence:
		if i != 0:
			decoded_sequence.append(index_word[i])
	return decoded_sequence


def encode_multiclass_labels(labels, num_classes):
	"""
	:param labels: list of labels
	:param num_classes: number of classes
	:return: encoded labels
	"""
	encoded_labels = np.zeros((len(labels), num_classes))
	for i, label in enumerate(labels):
		encoded_labels[i][label] = 1
	return encoded_labels


def decode_multiclass_labels(labels):
	"""
	:param labels: list of labels
	:return: decoded labels
	"""
	decoded_labels = []
	for i in labels:
		decoded_labels.append(np.argmax(i))
	return decoded_labels

class SimpleNN:
	def __init__(self, input_size, output_size, hidden_size, verbose=0):
		self.model = Sequential()
		self.model.add(Dense(hidden_size, input_dim=input_size, activation='relu'))
		self.model.add(Dense(output_size, activation='sigmoid'))
		self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
		if verbose:
			print(self.model.summary())

	def make_model(self, *args, **kwargs):
		return self.model

	def save_model(self, path):
		self.model.save(path)

	def load_model(self, path):
		self.model = load_model(path)

	def get_model(self):
		return self.model

	def get_weights(self):
		return self.model.get_weights()

	def set_weights(self, weights):
		self.model.set_weights(weights)

	def get_weights_as_image(self, *args, **kwargs):
		img = Image.new('RGB', (100, 100), color='red')
		model_weights = self.model.get_weights()
		tensors = []
		for i in range(len(model_weights)):
			tensors.append(torch.from_numpy(model_weights[i]))
		tensors = np.array(tensors, dtype=np.float32)
		tensors = tensors.resize(tensors.shape)
		img = Image.fromarray(np.uint8(img), 'RGB')
		img = np.uint8(np.clip(img, 0, 255).transpose((2, 0, 1)))
		img = img.astype(np.float32) / 255
		img = np.expand_dims(img, axis=0)
		img = np.expand_dims(img, axis=3)
		img = np.repeat(img, 3, axis=3)
		save_image(img, 'simpleNN_weights.png')
		return img

	def train(self, inputs, outputs, epochs=1000, verbose="auto"):
		self.model.fit(inputs, outputs, epochs=epochs, verbose=verbose, multiprocessing=True)

	def predict(self, inputs, verbose=0):
		predictions = self.model.predict(inputs)
		if verbose:
			print(predictions)
		return predictions

	@staticmethod
	def example(*args, **kwargs):
		# network learns XOR function, predicting 1 correctly
		print('XOR example: SimpleNN learns XOR function, predicting 1 correctly')
		inputs = [[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]]
		outputs = [0, 1, 1, 0]
		model = SimpleNN(3, 1, 4)

		model.train(inputs, outputs, epochs=1000, verbose=1)

		print('Predictions:')
		model.predict(inputs, verbose=1)

		print('Weights:')
		print(model.get_weights())

		print('Weights as image:')
		model.get_weights_as_image()

		print("That's it!")


# SimpleNN.example()



class SequentialANN:
	"""Simple class for training ANN to predict optimal parameters of any length. Output is simply
	0: bad, 1: good. In this example, network learns xor function from training set."""

	def __init__(self, input_size, output_size, hidden_size=5, epochs=10000, model_file=None, activation=None, verbose=0):
		self.input_size = input_size
		self.output_size = output_size
		self.hidden_size = None
		if isinstance(hidden_size, int):
			self.hidden_size = (hidden_size,)
		else:
			self.hidden_size = hidden_size
		self.epochs = epochs
		self.model_file = model_file
		self.verbose = verbose
		self.inputs, self.outputs = np.array(()), np.array(())
		self.model = Sequential()

		activation = {
			0: 'sigmoid',
			1: 'hard_sigmoid',
			2: 'relu',
			3: 'gelu',
			4: 'elu',
			5: 'selu',
			6: 'softmax',
			7: 'softplus',
			8: 'exponential',
			9: 'swish',
			10: 'linear'}

		for e in range(len(self.hidden_size)):
			if e == 0:
				# self.model.add(Dense(self.hidden_size[e], input_dim=input_size, activation="sigmoid",  kernel_initializer='uniform'))
				self.model.add(Dense(self.hidden_size[e], input_dim=input_size, activation=activation[0]))
			if e > 0:
				self.model.add(Dense(self.hidden_size[e], activation=activation[3], kernel_initializer='uniform'))
			# self.model.add(Dense(self.hidden_size[e],  activation="relu",  kernel_initializer='uniform'))
			# self.model.add(Dense(self.hidden_size[e],  activation="hard_sigmoid",  kernel_initializer='uniform'))
			# self.model.add(Dense(self.hidden_size[e],  activation="exponential",  kernel_initializer='uniform'))
			# self.model.add(Dense(self.hidden_size[e],  activation="elu",  kernel_initializer='uniform'))
			# self.model.add(Dense(self.hidden_size[e],  activation="exponential",  kernel_initializer='uniform'))

		self.model.add(Dense(output_size, activation=activation[0]))
		# self.model.add(Dense(output_size, activation="softmax"))
		# opt = keras.optimizers.Adam(learning_rate=0.01)
		opt = 'rmsprop'

		self.model.compile(loss="mean_absolute_error", optimizer=opt, metrics=['categorical_accuracy'])
		# self.model.compile(loss="mean_absolute_error", optimizer="rmsprop", metrics=['categorical_accuracy'])
		# self.model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['categorical_accuracy'])

		# self.model.compile(loss="mean_absolute_error", optimizer=opt, metrics=['categorical_accuracy'], run_eagerly=True)

		if self.model_file is not None:
			self.load()
		print("LAYER AMT:", len(self.model.get_config()['layers']))
		time.sleep(3)

	def train(self, inputs=None, outputs=None, epochs=None, verbose=None):
		if inputs is None:
			inputs = self.inputs
		else:
			inputs = np.array(inputs).astype('float32')
			# inputs = np.expand_dims(inputs, 0)
			# inputs = np.expand_dims(inputs, 0) / np.max(inputs)
		if outputs is None:
			outputs = self.outputs
		else:
			outputs = np.array(outputs).astype('float32')
			# outputs = np.expand_dims(outputs, 0)
		# print(inputs)
		# print(outputs)
		if epochs is None:
			epochs = self.epochs
		if verbose is None:
			verbose = self.verbose
		# steps = len(self.model.get_config()['layers']) * 1
		steps = self.input_size
		# steps = len(self.inputs)
		# steps = 10

		self.model.fit(inputs, outputs, epochs=epochs, steps_per_epoch=steps, verbose=verbose)

	def predict(self, inputs, verbose=0):
		a = np.array(inputs)
		if len(a.shape) == 1:
			a = np.expand_dims(a, 0)
		prediction = self.model.predict(a)
		if verbose == 1 and self.verbose == 1:
			print("Prediction:\n", prediction)
		return prediction

	def save(self, filename=None, verbose=1):
		if filename is None:
			filename = self.model_file
		self.model.save(filename)
		if verbose == 1 and self.verbose == 1:
			print(f'Model saved: {filename}')

	def load(self, filename=None):
		if filename is None:
			filename = self.model_file
		try:
			self.model = load_model(filename)
			print_boxed("Model load successful:", filename)
		except Exception:
			print(f'No model found: {filename}')

	def file_for_training(self, training_file, verbose=None, invert=0):
		inputs = []
		outputs = []
		with open(training_file) as f1:
			lines = f1.read()
			lines = lines.splitlines()
			for line in lines:
				line = eval(line)
				# print(line)
				# exit()
				# line = eval(line.replace("'", " "))
				if invert:
					inputs.append(line[0])
					outputs.append(line[1])
				else:
					inputs.append(line[1])
					outputs.append(line[0])
		self.inputs = np.array(inputs).astype('float32')
		self.outputs = np.array(outputs).astype('float32')
		if verbose is None:
			verbose = self.verbose
		if verbose is not None:
			print("INPUTS:", self.inputs)
			print("OUTPUTS:", self.outputs)
		return np.array(inputs).astype('float32'), np.array(outputs).astype('float32')


def SequentialANNexample():
	# network learns XOR function, predicting 1 correctly
	inputs = [[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]]
	outputs = [0, 1, 1, 0]

	a = SequentialANN(input_size=3, output_size=1, hidden_size=5, verbose=1)
	a.train(inputs, outputs, epochs=10000)

	predict = (1, 0, 0)
	a.predict(predict, verbose=1)
