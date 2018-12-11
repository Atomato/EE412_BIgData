import numpy as np

x = np.array([[3., 4., 5.],\
			[2., 7., 2.],\
			[5., 5., 5.],\
			[1., 2., 3.],\
			[3., 3., 2.],\
			[2., 4., 1.]])

y = np.array([1., 1., 1., -1., -1., -1.])

w = np.array([1., 1., 1.])
b = -10.

c = 0.2 # penalty of misclassification

w_len = sum(w*w)
margin = [y[j]*(sum(x[j]*w)+b) for j in range(len(x))]
print('Initial |w|: '+str(np.sqrt(w_len)))
for j in range(len(x)):
	print('Initial y(wx+b) '+str(j)+': '+str(margin[j]))
print('Initial cost: '+str(0.5*w_len + c*sum(max([0. for _ in range(len(x))], margin))))

lr = 0.1 # learning rate
for k in range(100000):
	print('\nIteration'+str(k))

	w_n = w # new w
	for i in range(len(w)):
		# gradient
		gd = w[i] + c*sum([(0 if y[j]*(sum(x[j]*w)+b) >= 1 else -y[j]*x[j][i]) \
														for j in range(len(x))])
		w_n[i] = w_n[i] - lr*gd

	gd = c*sum([(0 if y[j]*(sum(x[j]*w)+b) >= 1 else -y[j]) for j in range(len(x))])
	b = b - lr*gd
	w = w_n

	print('w: '+str(w))
	print('b: '+str(b))

	w_len = sum(w*w)
	margin = [y[j]*(sum(x[j]*w)+b) for j in range(len(x))]
	print('|w|: '+str(np.sqrt(w_len)))
	for j in range(len(x)):
		print('y(wx+b) '+str(j)+': '+str(margin[j]))
	print('cost: '+str(0.5*w_len + c*sum(max([0. for _ in range(len(x))], margin))))	