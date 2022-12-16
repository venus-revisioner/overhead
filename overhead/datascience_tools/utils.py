# coding=utf-8
import os

import numpy as np
import torch
from torchvision.utils import make_grid


def save_models(generator, discriminator, epochs):
	torch.save(generator.state_dict(), "saved_models/generator_%d.pth" % epochs)
	torch.save(discriminator.state_dict(), "saved_models/discriminator_%d.pth" % epochs)


def load_models(generator, discriminator, epochs, postfix=""):
	model_path = "saved_models"
	if postfix != "":
		model_path = f'{model_path}/{postfix}/'
		if not os.path.exists(model_path):
			os.makedirs(model_path)
	generator.load_state_dict(torch.load(f"{model_path}/generator_{epochs}.pth"))
	discriminator.load_state_dict(torch.load(f"{model_path}/discriminator_{epochs}.pth"))
	return epochs


def tensor_to_numpy(tensor):
	grid = make_grid(tensor.detach().cpu())
	# Add 0.5 after unnormalizing to [0, 255] to round to nearest integer
	ndarr = grid.permute(1, 2, 0).to("cpu", torch.float32).numpy()
	if ndarr.min() < 0:
		ndarr = grid.mul(0.5).add_(0.5).clamp_(0., 1.).permute(1, 2, 0).to("cpu", torch.float32).numpy()
	return np.rot90(ndarr.astype(np.float32), -1)


def load_model_latest_epoch(gen, disc, ep=0, postfix=""):
	model_path = "saved_models"
	if postfix != "":
		model_path = f'{model_path}/{postfix}'
	for file in os.listdir(model_path):
		if file.endswith(".pth"):
			ep = max(ep, int(file.split("_")[1].split(".")[0]))
	if ep > 0:
		ep = load_models(gen, disc, ep, postfix)
	return ep


def create_avg_losses_arbitrary_amount(loss_dict, window_size=32):
	loss_window = np.ones((window_size, len(loss_dict)))
	x = np.linspace(0, window_size, window_size, dtype=int)
	# for i, v in enumerate(loss_dict.values()):
	# 	x[:, i] = v
	# If at sample interval save image
	loss_head = f"\n# ------------windowed loss avg-------------- #"
	for i, v in enumerate(loss_dict.values()):
		loss_window[0, i] = loss_dict[v].item()
	avg_losses = f"\n"
	for i, v in enumerate(loss_dict.values()):
		avg_loss = np.sum(loss_window[:, v]) / loss_window.shape[0]
		loss_window = np.roll(loss_window, -1, axis=0)
		avg_losses += f"[avg_loss_{v}\t{avg_loss:.6f}]\t"
	print(loss_head)
	print(avg_losses)
	return avg_losses