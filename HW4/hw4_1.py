import sys

'''
	dot product
	https://stackoverflow.com/questions/32669855/dot-product-of-two-lists-in-python
'''
def dot(K, L):
	if len(K) != len(L):
		return 0
	return sum(i[0] * i[1] for i in zip(K, L))

with open(sys.argv[1], 'r') as f:
	with open(sys.argv[2], 'r') as l:
		feat = f.readlines() # features
		feat = list(map(lambda s: s.split(','),feat)) # split by comma
		feat = list(map(lambda l: list(map(float,l)),feat)) # change to integer
		N = len(feat) # the number of data

		lb = l.readlines() # labels
		lb = list(map(int, lb)) # change to integer

		# temp = list(map(lambda x: (x + 1)/2., lb))
		# print('temp', sum(temp)/N)

		# print('len feat', len(feat[0]))
		# print('feat[0]', feat[0])
		# print('len label', len(lb))
		# print('label[:10]', lb[:10])

		w = [0. for _ in range(len(feat[0]))]
		b = 0.

		c = 1 # penalty of misclassification
		lr = 0.05 # learning rate eta



		for k in range(50):
			print('iteration',k)
			w_n = w # new w
			margin = [lb[j]*(dot(feat[j],w)+b) for j in range(N)]

			for i in range(len(w)):
				# gradient
				gd = w[i] + c*sum([(0 if margin[j] >= 1 \
							else -lb[j]*feat[j][i]) for j in range(N)])
				w_n[i] = w_n[i] - lr*gd

			gd = c*sum([(0 if margin[j] >= 1 else -lb[j]) for j in range(N)])
			b = b - lr*gd
			w = w_n

			acc = sum([(1. if margin[j] > 0 else 0.) for j in range(N)])/N
			print('accuracy:', acc)


# x = np.array([[3., 4., 5.],\
# 			[2., 7., 2.],\
# 			[5., 5., 5.],\
# 			[1., 2., 3.],\
# 			[3., 3., 2.],\
# 			[2., 4., 1.]])

# y = np.array([1., 1., 1., -1., -1., -1.])

# w = np.array([1., 1., 1.])
# b = -10.

# c = 0.2 # penalty of misclassification

# w_len = sum(w*w)
# margin = [y[j]*(sum(x[j]*w)+b) for j in range(len(x))]
# print('Initial |w|: '+str(np.sqrt(w_len)))
# for j in range(len(x)):
# 	print('Initial y(wx+b) '+str(j)+': '+str(margin[j]))
# print('Initial cost: '+str(0.5*w_len + c*sum(max([0. for _ in range(len(x))], margin))))

# lr = 0.1 # learning rate
# for k in range(100000):
# 	print('\nIteration'+str(k))

# 	w_n = w # new w
# 	for i in range(len(w)):
# 		# gradient
# 		gd = w[i] + c*sum([(0 if y[j]*(sum(x[j]*w)+b) >= 1 else -y[j]*x[j][i]) \
# 														for j in range(len(x))])
# 		w_n[i] = w_n[i] - lr*gd

# 	gd = c*sum([(0 if y[j]*(sum(x[j]*w)+b) >= 1 else -y[j]) for j in range(len(x))])
# 	b = b - lr*gd
# 	w = w_n

# 	print('w: '+str(w))
# 	print('b: '+str(b))

# 	w_len = sum(w*w)
# 	margin = [y[j]*(sum(x[j]*w)+b) for j in range(len(x))]
# 	print('|w|: '+str(np.sqrt(w_len)))
# 	for j in range(len(x)):
# 		print('y(wx+b) '+str(j)+': '+str(margin[j]))
# 	print('cost: '+str(0.5*w_len + c*sum(max([0. for _ in range(len(x))], margin))))	