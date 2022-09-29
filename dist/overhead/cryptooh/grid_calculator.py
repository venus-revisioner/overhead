from pprint import pprint

import numpy as np


def grid_spacing(lo, hi, amt, decimals):
	grid = np.linspace(lo,hi,amt)
	grid = np.around(np.array(grid), decimals)
	# [print(i) for i in grid]
	# pprint(grid)
	return grid


# 1000LUNCBUSD Perpetual
grid_spacing(0.08, 0.170, 149, 4)

# BNBBUSD Perpetual
grid_spacing(200, 400, 149, 1)

#APEBUSD Perpetual
grid_spacing(4.3, 6.8, 149, 4)
