import time
import numpy as np

from keras.layers.core import Dense
from keras.models import Sequential, load_model


class SequentialANN:
	"""Simple class for training ANN to predict optimal parameters of any length. Output is simply
	0: bad, 1: good. In this example, network learns xor function from training set."""

	def __init__(self, input_size, output_size, hidden_size=5, epochs=10000, model_file=None, verbose=0):
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
