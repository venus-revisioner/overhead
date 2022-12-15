import os
import pathlib
import sys
import threading
import time
import random

import numpy as np
import cv2


from overhead.decooh import threaded_deco

python_path = "C:/python-3.10.7"
# check if the folder exists, if not, try to find it in PATH
if os.path.isdir(python_path):
	sys.executable = "C:/python-3.10.7/python.exe"
cv2.__load_extra_py_code_for_module("cv2", cv2.__collect_extra_submodules())


def record_video_to_disk(video_name='output.mp4', size=(720, 1280)):
	duration = 2
	fps = 30
	out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (size[1], size[0]), False)
	for _ in range(fps * duration):
		data = np.random.randint(0, 256, size, dtype='uint8')
		out.write(data)
	out.release()


def stream_webcam_to_disk(video_name='webcam.mp4'):
	cap = cv2.VideoCapture(0)
	fps = 30
	size = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

	out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, size, False)

	while True:
		ret, frame = cap.read()
		if ret != True:
			break
		out.write(frame)
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 255 == ord('q'):
			break
	cap.release()
	out.release()
	cv2.destroyAllWindows()


def load_video_to_numpy(video_name):
	cap = cv2.VideoCapture(video_name)
	while cap.isOpened():
		ret, frame = cap.read()
		if not ret:
			break
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 255 == ord('q'):
			break
	cap.release()
	cv2.destroyAllWindows()


def load_video_frames_to_numpy_array(filename):
	arr = {}
	cap = cv2.VideoCapture(filename)
	for i in range(1, int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
		ret, frame = cap.read()
		if ret:
			arr[i] = frame
	cap.release()
	return arr


def stream_webcam():
	cap = cv2.VideoCapture(0)
	while True:
		ret, frame = cap.read()
		if ret is False:
			break
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 255 == ord('q'):
			break
		if cv2.waitKey(1) & 255 == ord('s'):
			cv2.imwrite('screenshot.png', frame)
	cap.release()
	cv2.destroyAllWindows()


inter_flags = {'NEAREST': cv2.INTER_NEAREST,
			   'LINEAR': cv2.INTER_LINEAR,
			   'CUBIC': cv2.INTER_CUBIC,
			   'AREA': cv2.INTER_AREA,
			   'LANCZOS4': cv2.INTER_LANCZOS4,
			   'LINEAR_EXACT': cv2.INTER_LINEAR_EXACT,
			   'NEAREST_EXACT': cv2.INTER_NEAREST_EXACT,
			   'MAX': cv2.INTER_MAX,
			   'WARP_FILL_OUTLIERS': cv2.WARP_FILL_OUTLIERS,
			   'WARP_INVERSE_MAP': cv2.WARP_INVERSE_MAP}


class StreamWebcamThread(threading.Thread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.coeff = None
		self.cap = cv2.VideoCapture(0)
		self.dim = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		self.dim = np.array(self.dim)
		self.resize = None
		self.running = True
		self.pause_key = 32
		self.frame = None
		self.mod_func = None
		self.fps = 60
		self.resize = None

	def set_kwargs(self, kwargs=None):
		if kwargs is not None:
			print('setting kwargs', end=".")
			for k, v in kwargs.items():
				if hasattr(self, k):
					setattr(self, k, v)
					print(f"setting {k} to {v}")
				else:
					print(f"attribute {k} does not exist")
			time.sleep(2)

		if kwargs.get('mod_func'):
			self.mod_func = kwargs.get('mod_func')

		if kwargs.get('fps'):
			self.fps = kwargs.get('fps')

		if kwargs.get('resize'):
			self.resize = kwargs.get('resize')

		if kwargs.get('dim'):
			self.dim = kwargs.get('dim')

		if kwargs.get('coeff'):
			self.coeff = kwargs.get('coeff')

		if kwargs.get('pause_key'):
			self.pause_key = kwargs.get('pause_key')

		if kwargs.get('pause'):
			self.pause()

		if kwargs.get('resume'):
			self.resume()

		if kwargs.get('stop'):
			self.stop()

		if kwargs.get('start'):
			self.start()

		if kwargs.get('running'):
			self.running = kwargs.get('running')

		if kwargs.get('frame'):
			self.frame = kwargs.get('frame')

	def run(self):
			print(f'\rfps: {cv2.CAP_PROP_FPS}', end="")
			fps = self.cap.set(cv2.CAP_PROP_FPS, self.fps)
			print(f'\rfps: {fps}  ---   {cv2.CAP_PROP_FPS}', end="\n")

			low_dim = np.array(np.array(self.dim) * self.coeff).astype(np.int32)
			FPS = cv2.CAP_PROP_FPS

			print("#" + "-" * 50)
			while True:
				try:
					ret, self.frame = self.cap.read()

					if ret is False:
						continue
					else:
						if self.dim is not None:
							low_dim_arr = []

							self.frame = np.array(self.frame / 255., dtype=np.float32)
							# d = 1 / (2 ** 5)
							# self.frame, low_dim = self.resize_frame(self.dim, d, inter_flags['AREA'])
							# low_dim_arr.append(low_dim)
							d = 1 / (2 ** -1)
							self.frame, low_dim = self.resize_frame(self.dim, d, inter_flags['LANCZOS4'])
							low_dim_arr.append(low_dim)
							d = 1 / (2 ** 1)
							self.frame, low_dim = self.resize_frame(self.dim, d, inter_flags['AREA'])
							low_dim_arr.append(low_dim)
							d = 1 / (2 ** 0)
							self.frame, low_dim = self.resize_frame(self.dim, d, inter_flags['LANCZOS4'])
							low_dim_arr.append(low_dim)
							# d = 1 / (2 ** 3)
							# self.frame, low_dim = self.resize_frame(self.dim, d, inter_flags['LINEAR_EXACT'])
							# low_dim_arr.append(low_dim)
							# d = 1 / (2 ** -1)
							# self.frame, low_dim = self.resize_frame(self.dim, d, inter_flags['NEAREST'])
							# low_dim_arr.append(low_dim)

							# self.frame = np.power(self.frame, 2) * 1.333

							self.frame, low_dim = self.resize_frame(self.dim, 1., inter_flags['LANCZOS4'])
							low_dim_arr.append(low_dim)

							print(f'\rFPS: {FPS:.3f}\tlow dim: {low_dim_arr}\thigh dim: {self.dim}', end="")

							if cv2.waitKey(1) & 255 == ord('\x1b'):  # Escape
								break

							if cv2.waitKey(1) & 255 == self.pause_key:
								self.pause()
								self.resume()


						cv2.imshow('frame', self.frame)  # Show the frame

						self.take_screenshot("screenshot.png")

				except Exception as e:
					print(e)

				except KeyboardInterrupt:
					print('KeyboardInterrupt')
					self.stop()
					exit()

				except SystemExit() as e:
					print(e)
					self.stop()
					exit()

	def take_screenshot(self, path):
		if cv2.waitKey(1) & 255 == ord('s'):
			self.pause()
			cv2.imwrite(path, self.frame * 255.)
			print(f'\r\n--- Screenshot saved! ---', end="")
			self.resume()

	def get_frame(self):
		return self.frame

	def mod_frame(self):
		self.frame = self.mod_func(self.frame)
		return self.frame

	def resize_frame(self, source_dim, coeff, inter_flag):
		low_dim = np.array(source_dim) * coeff
		frame = cv2.resize(self.frame, low_dim.astype(np.int32), interpolation=inter_flag)
		return frame, tuple(low_dim.astype(np.int32))

	def resize_screen(self, dim=None, coeff=1):
		if dim is None:
			dim = self.dim
		if coeff is not None:
			dim = np.array(dim * coeff).astype(int)
		self.dim = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		return print(f'\rWebcam resolution: {self.dim}')

	def pause(self, sleep_time=0.5):
		self.pause_key = 32
		print('\fwebcam paused', end=".")
		time.sleep(sleep_time)
		return self.pause_key

	def resume(self, sleep_time=0.5):
		self.pause_key = None
		print('\fwebcam resumed', end=".")
		time.sleep(sleep_time)
		return self.pause_key

	def stop(self):
		self.running = False
		self.cap.release()
		cv2.destroyAllWindows()
		print('webcam stopped', end=".")


s = StreamWebcamThread()
s.set_kwargs({"dim": (1024, 1024), "coeff": 1 / (2 ** 5), "fps": 60 * 2, "mod_func": None})
s.start()


def stream_video(filename, *args, **kwargs):
	cap = cv2.VideoCapture(filename)
	frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	while True:
		ret, frame = cap.read()
		break_flag = show_with_loop(cap, ret, frame, frame_count, *args, **kwargs)
		if break_flag == 1:
			break
		else:
			cv2.imshow('frame', frame)
	cap.release()
	cv2.destroyAllWindows()


def show_with_loop(cap, ret, frame, frame_count, *args, **kwargs):
	if ret is False:
		return 1
	if kwargs.get('loop') is True and cap.get(cv2.CAP_PROP_POS_FRAMES) == frame_count:
		cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
		return 0
	if cv2.waitKey(1) & 255 == ord('q'):
		return 1


# def remove_video_background(filename, *args, **kwargs):
# 	cap = cv2.VideoCapture(filename)
# 	frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# 	fgbg = cv2.createBackgroundSubtractorMOG2()
# 	count = 0
# 	while True:
# 		count += 1
# 		ret, frame = cap.read()
# 		break_flag = show_or_loop(cap, ret, frame, frame_count, *args, **kwargs)
# 		# if (count < cap.get(cv2.CAP_PROP_FRAME_COUNT)):
# 		fgmask = fgbg.apply(frame)
# 		# cv2.imwrite('fgmask.jpg', fgmask)
# 		# cv2.imwrite('frame.jpg', frame)
# 		# frame = cv2.imread('frame.jpg')
# 		# fgmask = cv2.imread('fgmask.jpg')
# 		# im2, contours = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# 		# cv2.drawContours(frame, contours, -1, (0,255,0), 3)
# 		cv2.imshow('frame', fgmask)
#
# 		if break_flag == 1:
# 			break
# 			# if count % 1000 == 0:
# 			# 	cv2.imwrite('frame%d.jpg' % count, frame)
# 			# 	cv2.imwrite('fgmask%d.jpg' % count, fgmask)
# 	cap.release()
# 	cv2.destroyAllWindows()


def remove_video_background(filename, *args, **kwargs):
	blur = 3
	canny_low = 400
	canny_high = 512
	min_area = 1e-05
	max_area = 0.1
	dilate_iter, erode_iter = 2 ** 0, 2 ** 0
	mask_color = 0.0, 0.0, 0.0
	cap = cv2.VideoCapture(filename)
	frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	while True:
		ret, frame = cap.read()
		break_flag = show_with_loop(cap, ret, frame, frame_count, *args, **kwargs)
		if break_flag == 1:
			break
		image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(image_gray, canny_low, canny_high)
		edges = cv2.dilate(edges, None)
		edges = cv2.erode(edges, None)
		contour_info = [(c, cv2.contourArea(c)) for c in
						cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]]

		image_area = frame.shape[0] * frame.shape[1]
		maxx_area = max_area * image_area
		minn_area = min_area * image_area
		mask = np.zeros(edges.shape, dtype=np.uint8)
		for contour in contour_info:
			if contour[1] > minn_area and contour[1] < maxx_area:
				mask = cv2.fillConvexPoly(mask, contour[0], 255)
		mask = cv2.dilate(mask, None, iterations=dilate_iter)
		mask = cv2.erode(mask, None, iterations=erode_iter)
		mask = cv2.GaussianBlur(mask, (blur, blur), 0)
		mask_stack = np.dstack([mask] * 3).astype('float32') / 255.0
		frame = frame.astype('float32') / 255.0
		masked = mask_stack * frame + (1 - mask_stack) * mask_color
		masked = (masked * 255).astype('uint8')
		cv2.imshow('Foreground', masked)
	cap.release()
	cv2.destroyAllWindows()


def make_video_from_image(img_source, suffix="video", sec=1, auto_resolution=True):
	import cv2
	if auto_resolution:
		height, width, layers = img_source.shape
		size = (width, height)
	else:
		size = (640, 480)

	video_name = img_source.split('.')[0] + '_' + suffix + '.mp4'
	out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), sec, size, True)
	out.write(img_source)
	out.release()


# pycharm_path = Path(".").absolute().parents[1]
# janne_drag_path = pycharm_path.joinpath("Janne_drag")
# janne_video_catwalk = janne_drag_path.joinpath("janne_catwalk.mp4").__str__()

# stream_video(janne_video_catwalk, loop=True)
# remove_video_background(janne_video_catwalk, loop=True)

# remove_video_background(janne_video_catwalk, loop=1)
# video_arr = load_video_frames_to_numpy_array(janne_video_catwalk, video_arr)
# print(type(video_arr))
# print(len(video_arr))

# stream_webcam()


# def create_armature_model_from_video(video_source_file):
# 	v = cv2.VideoCapture(video_source_file)
# 	if not v.isOpened():
# 		raise IOError("Couldn't open webcam or video")
# 	video_FourCC = int(v.get(cv2.CAP_PROP_FOURCC))
# 	video_fps = v.get(cv2.CAP_PROP_FPS)
# 	video_size = (int(v.get(cv2.CAP_PROP_FRAME_WIDTH)),
# 				  int(v.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# 	isOutput = True if output_video_file != "" else False
# 	if isOutput:
# 		print("!!! TYPE:", type(output_video_file), type(video_FourCC), type(video_fps), type(video_size))
# 		out = cv2.VideoWriter(output_video_file, video_FourCC, video_fps, video_size)
# 	accum_time = 0
# 	curr_fps = 0
# 	fps = "FPS: ??"
# 	prev_time = timer()
# 	while True:
# 		return_value, frame = v.read()
# 		image = Image.fromarray(frame)
# 		image = yolo.detect_image(image)
# 		result = np.asarray(image)
# 		curr_time = timer()
# 		exec_time = curr_time - prev_time
# 		prev_time = curr_time
# 		accum_time = accum_time + exec_time
# 		curr_fps = curr_fps + 1
# 		if accum_time > 1:
# 			accum_time = accum_time - 1
# 			fps = "FPS: " + str(curr_fps)
# 			curr_fps = 0
# 		cv2.putText(result, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
# 					fontScale=0.50, color=(255, 0, 0), thickness=2)
# 		cv2.namedWindow("result", cv2.WINDOW_NORMAL)
# 		cv2.imshow("result", result)
# 		if isOutput:
# 			out.write(result)
# 		if cv2.waitKey(1) & 0xFF == ord('q'):
# 			break
# 	yolo.close_session()

@threaded_deco
def load_images_threaded(img_source, resize=None, mod_func=None):
	"""
	:param img_source: load img from file or give it as ndarray, and preprocess it
	:param resize: resize image to this size
	:param mod_func: modify image with this static function
	:return: preprocessed image as ndarray
	"""
	ext = ".jpg", ".png", ".jpeg", ".bmp", ".tiff", ".tif"
	img = None

	if img_source.is_dir():
		print("Cannot process directory in threaded way")
		return None
	elif isinstance(img_source, (list, tuple, set)) and len(img_source) < 2:
		img = np.array(img_source[0])
	elif isinstance(img_source, (list, tuple, set)) and len(img_source) > 1:
		print('Cannot process list of images in threaded way')
	elif img_source.is_file():
		if img_source.lower().endswith(ext):
			img = cv2.imread(img_source.__str__())
	else:
		print("Cannot process image source")
		return None

	if resize is not None:
		img = cv2.resize(img, resize, interpolation=cv2.INTER_AREA)
	if mod_func is not None:
		img = mod_func(img)
	return img


def sort_list(img_list, sort_type='asc'):
	"""
	:param img_list: list of images to sort
	:param sort_type: sort images by name, asc or desc, or randomize
	"""

	if sort_type == 'asc':
		img_list.sort()
	elif sort_type == 'desc':
		img_list.sort(reverse=True)
	elif sort_type == 'random':
		random.shuffle(img_list)

	return img_list


def img_resize(img, dim=(640, 480)):
	"""
	Resize a frame/img to a specific dimension
	:param img: frame/img to resize
	:param dim: dimension
	:return: resized frame/img
	"""
	return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


def load_images_to_list(imgs=None, resize=None, mod_func=None, sort_type='asc'):
	"""
	:param imgs: list of images to load, process or sort
	:param resize: resize image to this size
	:param mod_func: modify image with this static function
	:param sort_type: sort images by name, asc or desc, or randomize
	"""
	ext = ".jpg", ".png", ".jpeg", ".bmp", ".tiff", ".tif"
	img, img_list, img_path = None, [], []

	if imgs is None:
		print("No images to load")
		return None

	if isinstance(imgs, str):
		if not imgs.is_file():
			print('No file found')
			return None
		elif imgs.is_file() and imgs.lower().endswith(ext):
			print('File format not supported')
			return None

	elif os.path.isdir(imgs):
		for file in os.listdir(imgs):
			if file.lower().endswith(ext):
				img_list.append(load_images_threaded(file, resize, mod_func))
	elif isinstance(imgs, (list, tuple, set)) and len(imgs) > 1:
		for img in imgs:
			img_list.append(load_images_threaded(img, resize, mod_func))
	else:
		print("Cannot process image source")
		return None

	return img_list


class ImgStripToVideo:
	"""
	Converts a folder of images to a video.
	"""

	def __init__(self, source_folder, video_name, dim=(1920, 1080), fps='30', ordered='asc', mod_func=None):
		self.image_folder = source_folder
		self.video_name = video_name
		self.dim = dim
		self.fps = fps
		self.order = ordered
		self.mod_func = mod_func

		self.images = load_images_to_list(self.image_folder, resize=self.dim, sort_type=self.order, mod_func=mod_func)

	def make_video(self):
		"""	Make a video from a list of images. """

		out = cv2.VideoWriter(self.video_name, cv2.VideoWriter_fourcc(*'DIVX'), int(self.fps), self.dim)

		for i in range(len(self.images)):
			out.write(self.images[i])
		out.release()

		print(f'Video saved to {self.video_name}')

	def show_video(self):
		""" Show a video from a list of images. """

		for i in range(len(self.images)):
			cv2.imshow('frame', self.images[i])
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		cv2.destroyAllWindows()

	def show_video_threaded(self):
		""" Show a video from a list of images. """

		for i in range(len(self.images)):
			cv2.imshow('frame', self.images[i])
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		cv2.destroyAllWindows()
