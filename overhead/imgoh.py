import itertools

from PIL import Image


def cut_image_rectangles(img_path, amt=4):
	"""
	Cut images into rectangles and save them with indices inserted between postfix and name
	:param img_path: path to image
	:param amt: amount of rectangles to cut
	"""
	img = Image.open(img_path)
	width, height = img.size
	rects = []
	for i in range(amt):
		rects.extend(img.crop((width / amt * j,
		                       height / amt * i,
		                       width / amt * (j + 1),
		                       height / amt * (i + 1))) for j in range(amt))
	for i, rect in enumerate(rects):
		rect.save(f'rect_{i}_{img_path}')


def stitch_rectangles(img_path, rects_imgs):
	"""
	Stitch rectangles into image and save to disk with amt of rects between name and postfix
	:param img_path: path to image
	:param rects: list of rectangles
	:return: image
	"""
	img = Image.open(img_path)
	width, height = img.size
	rects = [Image.open(rect_img) for rect_img in rects_imgs]
	img = Image.new('RGB', (width, height))
	for i, j in itertools.product(range(amt), range(amt)):
		img.paste(rects[i * amt + j], (width / amt * j, height / amt * i))
	img.save(f'stitched_{amt}_{img_path}')


def use_multireso_without_padding(img_path, depth_amt):
	"""
	Use multi-resolution without padding to compress the image
	:param img_path: path to image
	:param depth_amt: amount of layers to use
	:return: image
	"""
	img = Image.open(img_path)
	width, height = img.size
	img = img.resize((width // depth_amt, height // depth_amt), Image.ANTIALIAS)
	img = img.resize((width, height), Image.ANTIALIAS)
	img.save(f'multireso_nopadding_{depth_amt}_{img_path}')
