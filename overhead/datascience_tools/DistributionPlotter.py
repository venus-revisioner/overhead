# coding=utf-8

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import vispy.plot as vp
from matplotlib.figure import Figure
from torch import Tensor


def DistributionPlotterVispy(data, bins=256):
	n_bins = 100
	fig = vp.Fig(show=False)
	line = fig[0:4, 0:4].plot(data, symbol='o', width=0, face_color=(1., 0.5, 0.1), edge_color=None, marker_size=6)
	line.set_gl_state(depth_test=False)
	fig[:, 0].histogram(data[:, 0], bins=n_bins, color=(1., 0., 0.), orientation='h')


@dataclass
class DistributionPlotter:
	img: np.ndarray = None
	z_tensor: Tensor = None
	plt: plt = plt
	fig: Figure = None
	sma_array = np.zeros(128)
	
	def __post_init__(self):
		self.start()
	
	def start(self, *args, **kwargs):
		self.plt.ion()
		self.plt.show(block=False)
		self.fig = self.plt.figure(figsize=(5, 10))
		self.fig.canvas.flush_events()
		self.fig.clear()
		return self.fig
	
	def distribution1D(self, *args, **kwargs):
		# plot the distribution of the noise in 1D
		ax1 = self.fig.add_subplot(3, 1, 1)
		ax1.set_title("1D distribution")
		ax1.hist(self.img.flatten(), bins=128)
	
	def distribution2D(self, *args, **kwargs):
		ax2 = self.fig.add_subplot(3, 1, 2)
		ax2.set_title("2D distribution")
		# plot the distribution of the noise in 2D
		ax2.scatter(self.img[:, 0], self.img[:, 1], s=1)
	
	def distribution3D(self, *args, **kwargs):
		# plot the distribution of the noise in 3D
		ax3 = self.fig.add_subplot(projection='3d')
		ax3.set_title("3D distribution")
		ax3.scatter(self.img[:, 0], self.img[:, 1], self.img[:, 2], s=1)
	
	def image(self, img=None, *args, **kwargs):
		if img is None:
			img = self.img
		ax4 = self.fig.add_subplot()
		ax4.set_title("Generated noise")
		ax4.imshow(img).autoscale()
	
	def time_distribution1D(self, plot_arrays, *args, **kwargs):
		if plot_arrays is None:
			plot_arrays = self.img
		# plot the evolution of loss function(s) over time
		# optionally add more loss functions to same plot
		# passing them as list or tuple
		# denote color to each one, and autoscale the y axis
		# add a legend to the plot
		# add a title to the plot
		# add a label to the x axis
		# add a label to the y axis
		# add a grid to the plot
		# add a marker to the plot
		# add a linestyle to the plot
		# add a linewidth to the plot
		# add a marker size to the plot
		# add a marker edge width to the plot
		# add a marker edge color to the plot
		
		ax5 = self.fig.add_subplot(3, 1, 3)
		for i, p in enumerate(plot_arrays):
			self.sma_array[0] = p
			self.sma_array = np.roll(self.sma_array, -1)
			sma_plt = self.sma_array / (self.sma_array).mean(keepdims=True)
			ax5.plot(sma_plt, label="loss_%d" % i, color="C%d" % i)
		ax5.set_title("1D distribution over time")
		ax5.set_xlabel("x")
		ax5.set_ylabel("y")
		ax5.grid(True)
		ax5.legend()  # add a legend to the plot
		ax5.autoscale()
	
	def draw(self):
		self.fig.tight_layout()
		self.fig.canvas.show()
		return self.fig
	
	def clear(self):
		self.fig.clear()
		self.fig.canvas.flush_events()
		return self.fig
	
	def drawing_plots(self, img_data, time_series=None, *args, **kwargs):
		self.clear()
		self.img = img_data
		self.distribution1D()
		self.distribution2D()
		# dp.distribution3D()
		# dp.image(img=tensor_to_numpy(gen_imgs.data))
		if time_series is not None:
			self.time_distribution1D(time_series)
		self.draw()
	
	def __call__(self, *args, **kwargs):
		self.start(*args, **kwargs)
		self.distribution1D(*args, **kwargs)
		self.distribution2D(*args, **kwargs)
		self.distribution3D(*args, **kwargs)
		self.image(*args, **kwargs)
		self.draw()
		return self.fig
	
	def __del__(self):
		plt.close(self.fig)