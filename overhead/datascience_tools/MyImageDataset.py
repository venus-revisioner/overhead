import os

import PIL.Image
import pandas as pd
import torch
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torchvision import transforms
from torchvision.io import read_image


def default_transforms(resize=64, to_float=True, normalize=False, to_tensor=False):
	transforms_list = []
	if to_float:
		transforms_list.append(transforms.ConvertImageDtype(torch.float32))
	if normalize:
		transforms_list.append(transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]))
	if resize:
		transforms_list.append(transforms.Resize(resize))
	if to_tensor:
		transforms_list.append(transforms.ToTensor())
	
	return transforms.Compose(transforms_list)


class MyImageDataset(Dataset):
	"""
	Args:
		annotations_file (string): Path to the csv file with annotations.
		img_dir (string): Directory with all the images.
		transform (callable, optional): Optional transform to be applied
			on a sample.
	Example:
			transform=transforms.Compose(
			[transforms.Resize(opt.img_size), transforms.ToTensor(), transforms.Normalize([0.5], [0.5])])

			These are transforms which will make the image 64x64, convert it to a tensor and normalize it

		target_transform (callable, optional): Optional transform to be applied
			on the target (e.g, label).
	"""
	
	def __init__(self, img_dir, label_dir=None, transform='default', target_transform=None, img_size=64):
		self.img_dir = img_dir
		self.label_dir = label_dir
		if label_dir is not None:
			self.labels = pd.read_csv(label_dir, skipinitialspace=False, header=0, sep=",")
			print(self.labels)
		self.img_size = img_size
		self.transform = transform
		if transform is None or transform == 'default':
			self.transform = default_transforms(self.img_size, to_float=True, normalize=True, to_tensor=False)
		self.target_transform = target_transform
		self.image_paths = [os.path.join(self.img_dir, self.labels.iloc[idx, 0]) for idx in range(len(self.labels))]
		print(f'Found {len(self.image_paths)} images in {self.img_dir}')
		self.images_as_tensors = [read_image(img_path) for img_path in self.image_paths]
		self.images_as_pil = [PIL.Image.open(img_path) for img_path in self.image_paths]
		print(f'Loaded {len(self.images_as_tensors)} images as tensors')
	
	def __len__(self):
		return len(self.labels)
	
	def __getitem__(self, idx):
		image = self.images_as_tensors[idx]
		lbl = self.labels.iloc[idx, 1]
		if self.transform is not None:
			image = self.transform(image)
		# image = self.transform(image) * 2. - 1.
		if self.target_transform:
			lbl = self.target_transform(lbl)
		
		# print(lbl, qimage.shape, image.dtype, image.min(), image.max())
		return image, lbl
	
	def get_image(self, idx):
		return self.images_as_pil[idx]
	
	def get_label(self, idx):
		return self.labels.iloc[idx, 1]
	
	def get_image_path(self, idx):
		return self.image_paths[idx]
	
	def get_image_as_tensor(self, idx):
		return self.images_as_tensors[idx]


class MyDataloader:
	def __init__(self, img_size=128, batch_size=1, num_workers=0, shuffle=True, transform='default', set_name='venus'):
		self.img_path, self.label_path = self.get_paths(set_name)
		self.batch_size = batch_size
		if batch_size is None:
			self.batch_size = len(os.listdir(self.img_path))
		self.num_workers = num_workers
		self.shuffle = shuffle
		self.img_size = img_size
		self.transform = transform
		self.dataset = MyImageDataset(img_dir=self.img_path, label_dir=self.label_path, img_size=self.img_size,
									  transform=self.transform)
		self.dataloader = DataLoader(self.dataset, batch_size=self.batch_size, shuffle=self.shuffle,
									 num_workers=self.num_workers, pin_memory=True)
		self.dataset_size = len(self.dataset)
		self.num_batches = len(self.dataloader)
		print(
				f'Created dataloader with {self.num_batches} batches of size {self.batch_size} and {self.num_workers} '
				f'workers')
	
	def get_dataset(self):
		return self.dataset
	
	def get_dataset_size(self):
		return self.dataset_size
	
	def get_num_batches(self):
		return self.num_batches
	
	def get_batch_size(self):
		return self.batch_size
	
	def get_num_workers(self):
		return self.num_workers
	
	@staticmethod
	def static_data(img_size=128, batch_size=1, num_workers=0, shuffle=True, transform='default', set_name='venus'):
		dataset = MyDataloader(img_size, batch_size, num_workers, shuffle, transform, set_name).dataset
		return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers, pin_memory=True)
	
	@staticmethod
	def static_dataloader(img_size=128, batch_size=1, num_workers=0, shuffle=True, transform='default',
						  set_name='venus'):
		return MyDataloader(img_size, batch_size, num_workers, shuffle, transform, set_name).dataloader
	
	@staticmethod
	def static_dataset(img_size=128, batch_size=1, num_workers=0, shuffle=True, transform='default', set_name='venus'):
		return MyDataloader(img_size, batch_size, num_workers, shuffle, transform, set_name).dataset
	
	@staticmethod
	def static_dataset_size(img_size=128, batch_size=1, num_workers=0, shuffle=True, transform='default'):
		return MyDataloader(img_size=img_size, batch_size=batch_size, num_workers=num_workers, shuffle=shuffle,
							transform=transform).dataset_size
	
	@property
	def prop_dataloader(self):
		return self.dataloader
	
	@property
	def prop_dataset(self):
		return self.dataset
	
	@property
	def prop_batch_size(self):
		return self.batch_size
	
	@property
	def prop_dataset_size(self):
		return self.dataset_size
	
	def get_paths(self, set_name):
		dict_paths = {
			"venus"   : (
			"D:/CODE_RESOURCES/my_pics/Venus_2k/", "D:/CODE_RESOURCES/my_pics/Venus_2k/Venus_2k_labels.cvs"),
			"4x4_grid": (
			"D:/CODE_RESOURCES/my_pics/4x4_grid/", "D:/CODE_RESOURCES/my_pics/4x4_grid/4x4_grid_labels.cvs")}
		self.img_path, self.label_path = dict_paths[set_name]
		return self.img_path, self.label_path
	
	def get_image(self, idx):
		return self.dataset.get_image(idx)  # self.dataset[idx][0]
	
	def get_label(self, idx):
		return self.dataset.get_label(idx)  # self.dataset[idx][1]
	
	def get_image_path(self, idx):
		return self.dataset.get_image_path(idx)
	
	def get_image_as_tensor(self, idx):
		return self.dataset.get_image_as_tensor(idx)