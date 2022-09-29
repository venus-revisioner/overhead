import cv2
import numpy as np


def record_video_to_disk(video_name='output.mp4', size=(720,1280)):
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
	cap.release()
	cv2.destroyAllWindows()


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

#
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
	dilate_iter, erode_iter = 2**0, 2**0
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
		contour_info = [(c, cv2.contourArea(c)) for c in cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]]

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
