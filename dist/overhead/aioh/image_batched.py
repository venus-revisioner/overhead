import numpy as np
import itertools
from PIL import Image
import keras
import tensorflow as tf


def tensorflow_batch_image_processing(img_path, depth_amt):
	import keras.utils.image_dataset as dt
	img = Image.open(img_path)
	width, height = img.size
	# img = tf.image.resize_with_pad(img, width // depth_amt, height // depth_amt)
	# img = tf.image.resize(img, width, height)
	# img.save(f'tf_batch_{depth_amt}_{img_path}')
	# img = dt.load_image(img_path)
	# width, height = img.size
	img = dt.image_utils.load_img(img)
	img = tf.image.resize_with_pad(img, width // depth_amt, height // depth_amt)
	img = tf.image.resize_with_pad(img, width, height)
	img_new = dt.image_utils.array_to_img(img[0])
	# img.save(f'tf_batch_{depth_amt}_{img_path}')


def load_image_as_keras_batches_to_array(image_path, depth_amt):
	import keras.utils.image_dataset as dt
	image = dt.image_utils.load_img(image_path)
	width, height = image.size
	arr = dt.image_utils.img_to_array(image)
	arr = np.array([arr])  # Convert single image to a batch."
	img = image.resize_with_pad(arr, width // depth_amt, height // depth_amt)
	img = image.resize_with_pad(img, width, height)
	image = dt.image_utils.save_img(f'tf_batch_{depth_amt}_{image_path}', img)


# image.save(f'tf_batch_{depth_amt}_{image_path}')
# predictions = model.predict(input_arr)


def tensor_batch_img_processing(image_path, depth_amt):
	"""
		The tensor_batch_img_processing function takes an image path and a depth amount, loads the image into memory,
		and then splits it up into smaller images of size (depth_amt x depth_amt) in batches. It then saves each
		batch as
		its own
		image file.

		:param image_path: Specify the path to the image that is to be processed
		:param depth_amt: Specify the number of batches to split the image into
		:return: A list of numpy arrays
		"""
	from tensorflow import image
	import keras.utils.image_dataset as dt
	img = dt.image_utils.load_img(image_path)
	width, height = img.size
	arr = dt.image_utils.img_to_array(image)
	img_tensor = np.expand_dims(arr, axis = 0)
	img_tensor /= 255.

	# create the batches
	img_tensor_batches = []
	for i, j in itertools.product (range (depth_amt), range (depth_amt)):
		img_tensor_batches.append (img_tensor[:,
		                           i * img_tensor.shape[1] // depth_amt: (i + 1) * img_tensor.shape[1] // depth_amt +
		                                                                 (1 if i == depth_amt - 1 else 0) *
		                                                                 img_tensor.shape[1] % depth_amt,
		                           j * img_tensor.shape[2] // depth_amt: (j + 1) * img_tensor.shape[2] // depth_amt + (
			                           1 if j == depth_amt - 1 else 0) * img_tensor.shape[2] % depth_amt, :])

	# process the batches
	img_tensor_batches_processed = []
	for img_tensor_batch in img_tensor_batches:
		img_tensor_batches_processed.append(img_tensor_batch)

	# stitch the batches
	img_tensor_new = np.zeros_like(img_tensor)
	for i, j in itertools.product(range(depth_amt), range(depth_amt)):
		img_tensor_new[:,
		i * img_tensor.shape[1] // depth_amt: (i + 1) * img_tensor.shape[1] // depth_amt + (
			1 if i == depth_amt - 1 else 0) * img_tensor.shape[1] % depth_amt,
		j * img_tensor.shape[2] // depth_amt: (j + 1) * img_tensor.shape[2] // depth_amt + (
			1 if j == depth_amt - 1 else 0) * img_tensor.shape[2] % depth_amt,
		:] = img_tensor_batches_processed[i * depth_amt + j]

	# save the image
	img_new = dt.image_utils.array_to_img(img_tensor_new[0])
	img_new.save(f'tf_batch_{depth_amt}_{image_path}')


def tensor_batch_img_processing_with_model(image_path, depth_amt, model_path):
	# now do the same but preparing for nn processing
	import keras.utils.image_dataset as dt
	image = dt.image_utils.load_img(image_path)
	width, height = image.size
	arr = dt.image_utils.img_to_array(image)
	img_tensor = np.expand_dims(arr, axis = 0)
	img_tensor /= 255.

	# create the batches
	img_tensor_batches = []
	for i, j in itertools.product(range(depth_amt), range(depth_amt)):
		img_tensor_batches.append(img_tensor[:,
		                          i * img_tensor.shape[1] // depth_amt: (i + 1) * img_tensor.shape[1] // depth_amt + (
			                          1 if i == depth_amt - 1 else 0) * img_tensor.shape[1] % depth_amt,
		                          j * img_tensor.shape[2] // depth_amt: (j + 1) * img_tensor.shape[2] // depth_amt + (
			                          1 if j == depth_amt - 1 else 0) * img_tensor.shape[2] % depth_amt,
		                          :])
		img_tensor_batches = np.array(img_tensor_batches)

		# create the model
		model = keras.models.load_model(model_path)
		model.summary()

		# evaluate the model
		img_tensor_batches_pred = model.predict(img_tensor_batches)

		# now we need to stitch the batches back together
		img_tensor_pred = np.zeros(img_tensor.shape)
		for i, j in itertools.product(range(depth_amt), range(depth_amt)):
			img_tensor_pred[:,
			i * img_tensor.shape[1] // depth_amt: (i + 1) * img_tensor.shape[1] // depth_amt + (
				1 if i == depth_amt - 1 else 0) * img_tensor.shape[1] % depth_amt,
			j * img_tensor.shape[2] // depth_amt: (j + 1) * img_tensor.shape[2] // depth_amt + (
				1 if j == depth_amt - 1 else 0) * img_tensor.shape[2] % depth_amt,
			:] = img_tensor_batches_pred[i * depth_amt + j]

		# now we need to convert the tensor back to an image
		img_pred = dt.image_utils.array_to_img(img_tensor_pred[0])
		img_pred = img_pred.resize((width, height))
		return img_pred


def tensor_img_processing_with_model(image_path, model_path):
	# now do the same but preparing for nn processing
	import tensorflow as tf
	import numpy as np
	import keras.utils.image_dataset as dt
	image = dt.image_utils.load_img (image_path)
	width, height = image.size
	arr = dt.image_utils.img_to_array (image)
	img_tensor = np.expand_dims (arr, axis = 0)
	img_tensor /= 255.

	# create the model
	model = tf.keras.models.load_model (model_path)
	model.summary()

	# evaluate the model
	img_tensor_pred = model.predict (img_tensor)

	# now we need to convert the tensor back to an image
	img_pred = dt.image_utils.array_to_img (img_tensor_pred[0])
	img_pred = img_pred.resize ((width, height))
	return img_pred


def tensor_img_processing_with_model_and_save(image_path, model_path, save_path):
	# now do the same but preparing for nn processing
	import tensorflow as tf
	import numpy as np
	import keras.utils.image_dataset as dt
	image = dt.image_utils.load_img (image_path)
	width, height = image.size
	arr = dt.image_utils.img_to_array (image)
	img_tensor = np.expand_dims (arr, axis = 0)
	img_tensor /= 255.

	# create the model
	model = tf.keras.models.load_model (model_path)
	model.summary ()

	# evaluate the model
	img_tensor_pred = model.predict (img_tensor)

	# now we need to convert the tensor back to an image
	img_pred = dt.image_utils.array_to_img (img_tensor_pred[0])
	img_pred = img_pred.resize ((width, height))
	img_pred.save (save_path)
	return img_pred


def tensor_img_processing_with_model_and_save_batch(image_paths, model_path, save_path):
	# now do the same but preparing for nn processing
	import tensorflow as tf
	import numpy as np
	import keras.utils.image_dataset as dt

	# create the model
	model = tf.keras.models.load_model (model_path)
	model.summary ()

	# evaluate the model
	for image_path in image_paths:
		image = dt.image_utils.load_img (image_path)
		width, height = image.size
		arr = dt.image_utils.img_to_array (image)
		img_tensor = np.expand_dims (arr, axis = 0)
		img_tensor /= 255.
		img_tensor_pred = model.predict (img_tensor)

		# now we need to convert the tensor back to an image
		img_pred = dt.image_utils.array_to_img (img_tensor_pred[0])
		img_pred = img_pred.resize ((width, height))
		img_pred.save (save_path)