import itertools
import random
import threading
import time

import numpy as np
import cupy as cp

from overhead.toolboxoh import TimeEval, print_topic, print_boxed, PermuteBruteForce
from overhead.visualizatioh import Canvas


class SomCupy(threading.Thread):
	def __init__(self, dim=(64*2, 64*2), max_iter=32 * 1, map_radius=1., neighb_pow=3.,
	             init_learn_rate=0.94, learn_rate_mode='const',
	             mex_hat_w=1., mex_hat_d=3., vec_len=1):

		threading.Thread.__init__(self)

		self.dim = dim
		self.max_iter = max_iter
		self.init_learn_rate = init_learn_rate
		self.learn_rate_mode = learn_rate_mode  # 'const' or 'var'
		self.neighb_diminish_rate = 1.
		self.neighb_pow = neighb_pow
		self.map_radius_div = 2.
		self.map_radius = map_radius
		self.mex_hat_width = mex_hat_w
		self.mex_hat_depth = mex_hat_d
		self.in_vector: cp.array = None
		self.weights: cp.array = cp.random.random((*self.dim, 1))
		self._mex_mat: cp.array = cp.ones((*self.dim, 1))
		self._influence: cp.array = cp.ones((*self.dim, 1))

		self._iterate = cp.int32(1)
		self._matrix: cp.meshgrid = None
		self._neighbourhood: cp.float = 1.
		self._learn_rate: cp.float = 1.
		self._BMU: cp.array = cp.zeros((2, 1, 1))
		self._dist: cp.array = cp.zeros((*self.dim, 1))
		self.real_coord = cp.array((0, 0), dtype=cp.int32)
		# self._map_radius: cp.array = cp.max(cp.array(self.dim)) / self.map_radius_div
		# self._map_radius = cp.sqrt(cp.max(cp.array(self.dim))) / (cp.sqrt(
		# self.neighb_pow)*1.9)
		self._map_radius = map_radius
		self._time_const = self.max_iter / cp.log(self._map_radius * self.neighb_diminish_rate)
		self.weights_out: np.array = np.zeros((*self.dim, 3))
		self._stop_sig = False
		self.iter_complete = False
		self.dim_cp = cp.array(self.dim)

	def run(self):
		timer = TimeEval()
		timer.start()
		self.iterator()
		sec = timer.stop()
		timer.get_time_str(verbose=1)


	def get_info(self):
		mem_pool = cp.get_default_memory_pool()
		mem_pool.set_limit(fraction=0.9)
		print("Current mempool limit", mem_pool.get_limit())

		print("IN VECTOR SIZE:", len(self._in_vector_array))
		print("TRAINING SIZE:", len(self._training_array))
		print()
		print(f'iteration: {self._iterate}')
		print(f'map radius: {self._map_radius}')
		print(f'time const: {self._time_const}')
		print(f'neighbourhood: {self._neighbourhood}')

	# @cp.fuse(kernel_name="SOM_lane")
	def adjust_vec_len(self, vec_len):
		self._dist = cp.array((*self.dim, len(vec_len)))
		self.weights_out = np.zeros((*self.dim, len(vec_len)))
		# self._time_const = self.max_iter / cp.log(self._map_radius * self.neighb_diminish_rate)
		self._time_const = len(self._training_array) / cp.log(self._map_radius * self.neighb_diminish_rate)
		self._influence: cp.array = cp.ones((*self.dim, len(vec_len)))
		self._mex_mat = cp.array((*self.dim, 1.))

	def make_matrix(self):
		mesh_x = cp.linspace(0, self.dim[ 0 ] - 1, self.dim[ 0 ])
		mesh_y = cp.linspace(0, self.dim[ 1 ] - 1, self.dim[ 1 ])
		self._matrix = cp.array(cp.meshgrid(mesh_x, mesh_y))

	@cp.fuse(kernel_name="SOM_lane")
	def learn_rate_eval(self):
		if self.learn_rate_mode == 'const':
			self._learn_rate = self.init_learn_rate
		if self.learn_rate_mode == 'var':
			self._learn_rate = self.init_learn_rate * cp.exp(-self._iterate / self._time_const)

	@cp.fuse(kernel_name="SOM_lane")
	def neighb_eval(self):
		self._neighbourhood = self._map_radius * cp.exp(-self._iterate / self._time_const)

	@cp.fuse(kernel_name="SOM_lane")
	def find_nearest(self):
		ind = cp.argmin(cp.sqrt(cp.sum(cp.square(self.in_vector - self.weights), axis=2)))
		# ind = cp.argmin(cp.sqrt(cp.sum(cp.square(self.weights - self.in_vector),
		# axis=2)))
		BMU = cp.array(cp.round((cp.mod(ind, self.dim[ 0 ]), cp.mod((ind / self.dim_cp[ 1 ]), self.dim_cp[ 1 ])), 1))
		self._BMU = cp.reshape(BMU, (2, 1, 1))

	@cp.fuse(kernel_name="SOM_lane")
	def distance_in_plane(self):
		# self._dist = cp.reshape(cp.sqrt(cp.sum(cp.square(self._matrix - self._BMU),
		# axis=0)), (*self.dim, 1))
		self._dist = cp.expand_dims(cp.sqrt(cp.sum(cp.square(self._BMU - self._matrix), axis=0)), 2)

	# self._dist = cp.expand_dims(cp.sqrt(cp.sum(cp.square(self._matrix-self._BMU),
	# axis=0)), 2)

	@cp.fuse(kernel_name="SOM_lane")
	def distance_in_torus(self):
		shifter0 = self._BMU[ 0 ] + (self.dim[ 0 ] / 2.)
		shifter1 = self._BMU[ 1 ] + (self.dim[ 0 ] / 2.)
		real_c = cp.roll(cp.array(self._matrix) - cp.array((self.dim[ 0 ] / 2.)),
		                 cp.array((shifter1, shifter0), dtype=cp.int32), axis=(1, 2))

		self._dist = cp.expand_dims(cp.sqrt(cp.sum(cp.square(real_c), axis=0)), 2)

	@cp.fuse(kernel_name="SOM_lane")
	def ricker_wavelet(self):
		"""
		The ricker_wavelet function creates a Mexican hat wavelet.
		The function takes three parameters:
		- self : the class object itself, which is used to access its attributes and methods.
		- f : the width of the wavelet in Hz (default = 10).  The larger this value, the wider it will be.
		This parameter should not exceed half of your sampling frequency (i.e., if you're sampling at 1000Hz,
		then f should not exceed 500).
		- depth : how deep or shallow you want your wavelet to be (default = 1).
		:param self: Access variables that belongs to the class
		:return: A 3d array of the mexican hat wavelet
		"""
		# print(self._mex_mat.shape)
		f = self.mex_hat_width
		sca = (1000 * cp.divide(self.dim_cp, cp.array((256., 256.))))
		length = self.dim_cp / (1000 * (self.dim_cp / 256.))
		dt = 1 / sca
		mat_x = self._dist * (self.dim_cp / self._neighbourhood) * dt * length
		mat_y = (1.0 - 2.0 * cp.power(cp.pi, 2.) * cp.power(f, 2.) * cp.power(mat_x, 2.)) * (
				cp.exp(-cp.power(cp.pi, 2.) * cp.power(f, 2.) * cp.power(mat_x, 2.)))


		# MY ORDINARY VERSION
		# mat_x = cp.expand_dims(mat_x, 2)
		# mex_min = cp.maximum(-1., mat_y * self.mex_hat_depth)
		# mex_max = cp.minimum(1., mex_min * self.mex_hat_depth)
		# coeff = (self.mex_hat_depth * (mex_min + mex_max) / 2.)
		# self._dist = self._dist - cp.sqrt(coeff[:, :, 1]*coeff[:, :, 1] - coeff[:, :, 0]*coeff[:, :, 0]).reshape(self._dist.shape)


		# VERY INTERESTING 3D SHAPE!
		mat_x = cp.expand_dims(mat_x, 2)
		mex_min = cp.maximum(-1., mat_y * self.mex_hat_depth)
		mex_max = cp.minimum(1., mex_min * self.mex_hat_depth)
		coeff = (self.mex_hat_depth * (mex_min - mex_max)) ** 3.
		self._dist = self._dist - cp.sqrt(coeff[:, :, 1]*coeff[:, :, 1] - coeff[:, :, 0]*coeff[:, :, 0]).reshape(self._dist.shape)



	@cp.fuse(kernel_name="SOM_lane")
	def influence_eval(self):
		# inf = cp.exp(-cp.square(self._dist)/(2.*cp.square(self._neighbourhood)))
		inf = cp.exp(-(self._dist * self._dist) / (2. * self._neighbourhood * self._neighbourhood))
		self._influence = cp.dstack((inf, inf, inf))

	@cp.fuse(kernel_name="SOM_lane")
	def update_weights(self):
		# is_within = self._dist < ((self._neighbourhood) ** self.neighb_pow)
		# self.weights = self.weights + self._learn_rate * self._neighbourhood * (
		# self.in_vector - self.weights) \
		#                * cp.less(self._dist, self._neighbourhood ** self.neighb_pow)
		self.weights = self.weights + self._learn_rate * self._influence * (self.in_vector - self.weights)\
		               * cp.less(self._dist, self._neighbourhood ** self.neighb_pow)

	@cp.fuse(kernel_name="SOM_lane")
	def iterate(self):
		# self.in_vector = arr[0]
		# self.in_vector = arr
		self.learn_rate_eval(self)
		self.neighb_eval(self)
		self.find_nearest(self)
		# self.distance_in_plane(self)
		self.distance_in_torus(self)
		self.ricker_wavelet(self)
		self.influence_eval(self)
		self.update_weights(self)

	def iterator(self):
		"""
		Make sure every data point possible is loaded onto GPU before invoking this loop.
		Unfortunately the process could not be pararrelized, as the learning happens in
		one domain at a time. Of course its possible run chained, or parallell processes...
		"""
		# PermuteBruteForce([self._training_array]).with_function(self.iterate_step)
		# [self.iterate_step() for i in self._training_array]
		self.get_info()

		cycle_in_vec = itertools.cycle(self._in_vector_array)
		for ve in self._training_array:
			if self._stop_sig:
				break
			self.in_vector = next(cycle_in_vec)
			self.iterate(self)
			self._iterate = cp.add(self._iterate, 1)

		# while self._iterate < len(self._training_array):
		# 	self.in_vector = self._training_array[self._iterate]
		# 	self.iterate_step(self)

		print_topic("ITERATION FINISHED")
		self.iter_complete = True
		self.get_info()

	def train(self, in_vector):
		self._in_vector_array = cp.array(in_vector)
		self._training_array = cp.array(in_vector * self.max_iter)
		self.max_iter = len(self._training_array)
		self.adjust_vec_len( in_vector[0])
		self.make_matrix()
		self.start()

	def stop(self):
		self._stop_sig = True

	@property
	def get_weights(self):
		weights = cp.ones(self.weights.shape)
		cp.copyto(weights, self.weights)
		return weights.get()

	def predict(self, input_vector):
		self.in_vector = cp.array(input_vector)
		# self.train(input_vector)
		self.find_nearest(self)
		# self.distance_in_plane(self)
		self.distance_in_torus(self)
		p = cp.squeeze(self._dist)
		avg_point = int(round(cp.average(p[ 0 ]).tolist(), 0)), int(round(cp.average(p[ 1 ]).tolist(), 0))
		# avg_point =  cp.divide(cp.sum(p[0]),len(p[0])).tolist(), cp.divide(cp.sum(p[
		# 1]),len(p[1])).tolist()
		# self.weights[avg_point[0],avg_point[1]] = cp.array((1.,1.,1.))
		temp_weights = self.weights
		self.weights = (1. - cp.greater(self._dist, 0.95))
		self.in_vector = cp.array((1., 1., 1.))
		self.find_nearest(self)
		self.weights = temp_weights + (1. - cp.greater(self._dist, 0.95))
		# self.weights += temp_weights
		# return avg_point
		return self._BMU.squeeze()


class SomWorker(SomCupy):
	def __init__(self, *args, **kwargs):
		SomCupy.__init__(self, *args, **kwargs)
		self.sc = SomCupy
		self.canvas = Canvas(tex_size=self.dim, canvas_sca=0.85)
		self.canvas.texture.interpolation = "nearest"
		self._training_pool = None
		self._iter_permute = 0
		self._iter_counter = 0
		self._prediction = None

	def train(self, training_pool):
		self._training_pool = training_pool
		self.sc.train(self, training_pool)

	def stop(self):
		self._stop_sig = True
		self.canvas.stop = True

	def demo_rgb(self, color_amt=5):
		print(f'DEMO: COLOR AMT {color_amt ** 3}\n')
		# generate initial data_tools into an array
		array_pool = [ np.linspace(0., 1., color_amt).tolist() ] * 3
		perm = PermuteBruteForce(array_pool)

		# allocate training pool
		self._training_pool = tuple(perm.permuted)
		self._map_radius = np.sqrt(self.dim[ 0 ] * len(array_pool) + 1)

		# start training SOM
		self.train(self._training_pool)
		# self.get_info()

		# predict all for demo purposes
		self.predict_all()

	def predict_vector(self, p):
		self._prediction = self.predict(p)
		location = self._prediction[ ::-1 ]
		print(f'PREDICTING {self._iter_permute}: {p} -- LOCATION: {location}')
		self.canvas.injection(self.get_weights)
		return location

		# p = self._training_pool[iter_permute % len(self._training_pool) ]
		# prediction = self.predict(p)
		# print(f'PREDICTING {iter_permute}: {p} -- LOCATION: {prediction[ ::-1 ]}')
		# prediction = None

		# self._iterate = cp.add(self._iterate, 1) % len(self._in_vector_array)

	def predict_all(self):
		"""
		The predict_all function is a function that is called every 1/60th of a second.
		It will iterate through the training pool and predict the location of each image in the training pool.
		The prediction is printed to console, along with which iteration it's on.

		:param self: Access the class attributes
		:return: The location of the prediction
		"""
		iter_permute = 0
		iter_counter = 0
		while True:
			if self.canvas._closed:
				self.stop()
				break
			if not self.iter_complete:
				time.sleep(1 / 60.0)
			else:
				if iter_permute < len(self._training_pool) and iter_counter % 10 == 0:

					p = self._training_pool[ iter_permute % len(self._training_pool) ]
					prediction = self.predict(p)
					print(f'PREDICTING {iter_permute}: {p} -- LOCATION: {prediction[ ::-1 ]}')
					prediction = None

					iter_permute += 1

				if iter_permute == len(self._training_pool):
					print_boxed("PREDICTION COMPLETED")
					print("PRESS ESC TO EXIT...")
					iter_permute += 1

				# unless... testing some possible iterpolation functionality
				else:
					# self.move_test(iter_permute)
					# iter_permute += 1
					pass

			self.canvas.injection(self.get_weights)
			iter_counter += 1

	def move_test(self, iter_permute):
		self._iterate = len(self._training_array) * 0.7
		self.neighb_pow = 4.
		self.mex_hat_width = 3.
		self.mex_hat_depth = 10.
		# p = self._training_pool[iter_permute % len(self._training_pool)]
		p = random.choice(self._training_pool)
		self.in_vector = cp.array(p)
		self.weights += (cp.random.uniform(-0.0005, 0.0005, self.weights.shape))
		self.iterate(self)


SomWorker().demo_rgb(color_amt=5)
