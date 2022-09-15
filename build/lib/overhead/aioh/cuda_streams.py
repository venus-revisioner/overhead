import threading
import cupy as cp


class CupyArrayStream(threading.Thread):
	def __init__(self, arr=None, stream=None, use_canvas=None):
		threading.Thread.__init__(self)

		self.arr = arr
		self.stream = stream
		self.canvas = use_canvas
		self.canvas = use_canvas
		# self.get_stream_name()

	def run(self):
		self.canvas.rgb_inject = cp.asnumpy(self.arr, self.stream)

	def get_stream_name(self):
		print(self.__str__())


class CupyFunctionStream(threading.Thread):
	def __init__(self, func=None, stream=None, use_canvas=None):
		"""
		It takes a function, a stream, and a canvas, and then it runs the function on the
		stream, and then it streams the output to the canvas

		Args:
		  func: a function that takes in a time parameter and returns a complex array
		  stream: the stream to use for the thread
		  use_canvas: the canvas object that the stream will be drawing to
		"""
		threading.Thread.__init__(self)
		if func is None:
			func = []
		self.func_fusion = func
		self.stream = stream
		self.canvas = use_canvas
		self.c_matrix = cp.zeros(())
		self.arr_out = cp.zeros(())
		self.stop_flag = 0
		self.canvas.timer_toggle = 1
		self.canvas.timer_verbose = 0
		self.timer = 0.0
		self.timer_scale = 1.0
		self.timer_offset = 0
		self.func_dict = {}
		self.arr_feedback = cp.ones(self.canvas.tex_size, dtype=cp.complex64)
		# self.cp_array_stream = CupyArrayStream(use_canvas=self.canvas, stream=self.stream)

	def run(self):
		with self.stream:
			self.get_stream_name()
			self.draw_loop()

	def stream_array(self, a):
		CupyArrayStream(a, self.stream, self.canvas).run()

	def draw_loop(self):
		while not self.stop_flag:
			if self.canvas._timer.running:
				self.timer = self.canvas.timer * self.timer_scale + self.timer_offset

				self.func_eval()
				self.stream_array(self.arr_out)

				self.stop_stream()

	def func_eval(self):
		# self.arr_out = [f for f in self.func_fusion]
		# for f in self.func_fusion:
		#     self.arr_out = f

		f = self.func_dict['function'][0]
		self.arr_out = self.func_init(f)

	def func_init(self, func):
		# kwargs = self.kwargs
		# fw = f.__code__.co_varnames
		# u = set(kwargs.keys()).difference(fw)
		# for i in u:
		#     print(f)
		#     print(i)
		#     del kwargs[i]
		#     print(kwargs.keys())

		func['kwargs']['t'] = self.timer
		# func['kwargs']['c'] = self.c_matrix * self.arr_out
		return func['code'](**func['kwargs'])

	def get_stream_name(self):
		print(self.__str__())

	def stop_stream(self):
		if self.stop_flag:
			print(f"{self.__str__()} QUIT")
			self.canvas.stop_flag = 1
			assert self.stream == cp.cuda.get_current_stream()



def cp_min_max(a, verbose=0):
	"""
	The cp_min_max function computes the minimum and maximum values of a given array.
	It returns two values, the first being the minimum value and second being the maximum value.

	:param a: Pass in the array to be checked
	:param verbose=0: Turn off the print statements
	:return: The minimum and maximum values of the array a
	:doc-author: Trelent
	"""
	if verbose:
		print()
		print("**** Min:", cp.min(a), "--- Max:", cp.max(a), "****")
		print()
	return cp.min(a), cp.max(a)


def cp_normalize(a, r=None):
	r_min, r_max = r if r is not None else (0., 1.)
	a_min, a_max = cp_min_max(a)
	return (((a - a_min) * (r_max - r_min)) / (a_max - a_min)) + r_min
