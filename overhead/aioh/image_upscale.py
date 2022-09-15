import itertools

from tensorflow.lite.python.schema_py_generated import np


def upscale_tensor(img_tensor_batch, factor=4):
	import keras.utils.image_dataset as dt
	img_tensor_batch = dt.image_utils.get_interpolation('area').resize(img_tensor_batch,
	                                                                   [img_tensor_batch.shape[1] * factor,
																		img_tensor_batch.shape[2] * factor])
	img_tensor_batch = img_tensor_batch.numpy()
	return img_tensor_batch


# Decorator version of the upscaling function
def upscale_batch(batch, upscale_func=upscale_tensor, factor=4):
	for b in batch:
		upscale_func(b, factor)
	return batch


def tensor_batch_img_processing(image_path, depth_amt):
	from tensorflow import image
	import keras.utils.image_dataset as dt
	img = dt.image_utils.load_img(image_path)
	width, height = img.size
	arr = dt.image_utils.img_to_array(image)
	img_tensor = np.expand_dims(arr, axis = 0)
	img_tensor /= 255.
	# create the batches
	img_tensor_batches = [ ]
	for i, j in itertools.product(range(depth_amt), range(depth_amt)):
		img_tensor_batches.append(img_tensor[ :, i * img_tensor.shape[ 1 ] // depth_amt: (i + 1) * img_tensor.shape[
			1 ] // depth_amt + (1 if i == depth_amt - 1 else 0) * img_tensor.shape[ 1 ] % depth_amt,
		                          j * img_tensor.shape[ 2 ] // depth_amt: (j + 1) * img_tensor.shape[
			                          2 ] // depth_amt + (1 if j == depth_amt - 1 else 0) * img_tensor.shape[
			                                                                  2 ] % depth_amt, : ])

	# process the batches
	img_tensor_batches_processed = [ ]
	for img_tensor_batch in img_tensor_batches:
		"""
		HERE THE UPSCALING FUNCTION
		"""
		img_tensor_batches_processed.append(img_tensor_batch)

	# stitch the batches
	img_tensor_new = np.zeros_like(img_tensor)
	for i, j in itertools.product(range(depth_amt), range(depth_amt)):
		img_tensor_new[ :, i * img_tensor.shape[ 1 ] // depth_amt: (i + 1) * img_tensor.shape[ 1 ] // depth_amt + (
				1 if i == depth_amt - 1 else 0) * img_tensor.shape[ 1 ] % depth_amt,
		j * img_tensor.shape[ 2 ] // depth_amt: (j + 1) * img_tensor.shape[ 2 ] // depth_amt + (
				1 if j == depth_amt - 1 else 0) * img_tensor.shape[ 2 ] % depth_amt, : ] = img_tensor_batches_processed[
			i * depth_amt + j ]

	# save the image
	img_new = dt.image_utils.array_to_img(img_tensor_new[ 0 ])
	img_new.save(f'tf_batch_{depth_amt}_{image_path}')


# Example:
def upscaling_decorator_example(image_path, depth_amt, upscale_func=upscale_batch, factor=4):
	from tensorflow import image
	import keras.utils.image_dataset as dt
	img = dt.image_utils.load_img(image_path)
	width, height = img.size
	arr = dt.image_utils.img_to_array(image)
	img_tensor = np.expand_dims(arr, axis=0)
	img_tensor /= 255.

	# create the batches
	img_tensor_batches = [ ]
	for i, j in itertools.product(range(depth_amt), range(depth_amt)):
		img_tensor_batches.append(img_tensor[ :, i * img_tensor.shape[ 1 ] // depth_amt: (i + 1) * img_tensor.shape[
			1 ] // depth_amt + (1 if i == depth_amt - 1 else 0) * img_tensor.shape[ 1 ] % depth_amt,
		                          j * img_tensor.shape[ 2 ] // depth_amt: (j + 1) * img_tensor.shape[
			                          2 ] // depth_amt + (1 if j ==
			                                             depth_amt - 1 else 0) * img_tensor.shape[ 2 ] % depth_amt, : ])

	# process the batches
	img_tensor_batches_processed = [ ]
	for img_tensor_batch in img_tensor_batches:
		img_tensor_batches_processed.append(upscale_func(img_tensor_batch, upscale_func=upscale_func, factor=factor))

	# stitch the batches
	img_tensor_new = np.zeros_like(img_tensor)
	for i, j in itertools.product(range(depth_amt), range(depth_amt)):
		img_tensor_new[ :, i * img_tensor.shape[ 1 ] // depth_amt: (i + 1) * img_tensor.shape[ 1 ] // depth_amt + (
				1 if i ==
				depth_amt - 1 else 0) * img_tensor.shape[ 1 ] % depth_amt,
		j * img_tensor.shape[ 2 ] // depth_amt: (j + 1) * img_tensor.shape[ 2 ] // depth_amt + (
				1 if j ==
				depth_amt - 1 else 0) * img_tensor.shape[ 2 ] % depth_amt, : ] = img_tensor_batches_processed[
			i * depth_amt + j ]

	# save the image
	img_new = dt.image_utils.array_to_img(img_tensor_new[ 0 ])
	img_new.save(f'tf_batch_{depth_amt}_{image_path}')


# Create the decorator with the upscaling functions and the input image
def upscale_wrapper(image_path, upscale_func=upscale_batch, factor=4):
	"""
	The upscale_wrapper function is a decorator that takes an image path as input and returns the processed image.
	The function is decorated by the upscale_wrapper function which takes in an upscale_func, factor, and depth_amt as
	arguments.
	The upscale func can be any of the functions defined above (upscale or upsample). The factor is used to determine
	how much to scale up by.
	Depth amt determines how many times we want to apply this process recursively.

	:param image_path: Pass the path to the image that is being processed
	:param upscale_func = upscale_batch: Pass the function used to upscale the image
	:param factor = 4 : Determine the size of the image
	:return: A function that takes a depth amount and returns the image processed by the upscale_batch function
	"""
	def wrapper(func):
		def image_processing(depth_amt):
			from tensorflow import image
			import keras.utils.image_dataset as dt
			img = dt.image_utils.load_img(image_path)
			width, height = img.size
			arr = dt.image_utils.img_to_array(image)
			img_tensor = np.expand_dims(arr, axis=0)
			img_tensor /= 255.

			# create the batches
			img_tensor_batches = [ ]
			for i, j in itertools.product(range(depth_amt), range(depth_amt)):
				img_tensor_batches.append(img_tensor[ :, i * img_tensor.shape[ 1 ] // depth_amt: (i + 1) *
				img_tensor.shape[
					1 ] // depth_amt + (1 if i == depth_amt - 1 else 0) * img_tensor.shape[ 1 ] % depth_amt,
				                          j * img_tensor.shape[ 2 ] // depth_amt: (j + 1) * img_tensor.shape[
					                          2 ] // depth_amt + (1 if j == depth_amt - 1 else 0) * img_tensor.shape[
					                                                                  2 ] % depth_amt, : ])

			# process the batches
			img_tensor_batches_processed = [ ]
			for img_tensor_batch in img_tensor_batches:
				img_tensor_batches_processed.append(upscale_func(img_tensor_batch, upscale_func=upscale_func, factor=factor))

			# stitch the batches
			img_tensor_new = np.zeros_like(img_tensor)
			for i, j in itertools.product(range(depth_amt), range(depth_amt)):
				img_tensor_new[ :, i * img_tensor.shape[ 1 ] // depth_amt: (i + 1) * img_tensor.shape[ 1 ] // depth_amt + (
						1 if i == depth_amt - 1 else 0) * img_tensor.shape[ 1 ] % depth_amt,
				j * img_tensor.shape[ 2 ] // depth_amt: (j + 1) * img_tensor.shape[ 2 ] // depth_amt + (
						1 if j == depth_amt - 1 else 0) * img_tensor.shape[ 2 ] % depth_amt, : ] = img_tensor_batches_processed[
					i * depth_amt + j ]

			# save the image
			img_new = dt.image_utils.array_to_img(img_tensor_new[ 0 ])
			img_new.save(f'tf_batch_{depth_amt}_{image_path}')
		return image_processing
	return wrapper