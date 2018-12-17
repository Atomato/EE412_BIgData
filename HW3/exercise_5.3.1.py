import numpy as np

trans_mat = [[0., 1./2, 1., 0],\
			[1./3, 0., 0., 1./2],\
			[1./3, 0., 0., 1./2],\
			[1./3, 1./2, 0., 0.]]

b = 0.8 # taxation constant beta
# teleport = np.array([1., 0., 0., 0.]) # teleport set = {A}
teleport = np.array([1./2, 0., 1./2, 0.]) # teleport set = {A, C}
v = teleport # start with the pages in the teleport set

for _ in range(50):
	v = b*np.matmul(trans_mat, v) + (1-b)*teleport
print('')
print(v)
print('')