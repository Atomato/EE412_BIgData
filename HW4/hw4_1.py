# python 2.7
import sys

'''
	dot product
	https://stackoverflow.com/questions/32669855/dot-product-of-two-lists-in-python
'''
def dot(K, L):
	if len(K) != len(L):
		return 0
	return sum(i[0] * i[1] for i in zip(K, L))

with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'r') as l:
	feat_e = f.readlines() # entire features
	feat_e = list(map(lambda s: s.split(','),feat_e)) # split by comma
	feat_e = list(map(lambda l: list(map(float,l)),feat_e)) # change to number

	N_e = len(feat_e) # the number of data
	dim = len(feat_e[0]) # features size

	lb_e = l.readlines() # entire labels
	lb_e = list(map(float, lb_e)) # change to number

	acc_test = []
	for cv in range(10):
		test_n = N_e/10 # size of test chunk
		test_f = feat_e[(test_n*cv):(test_n*cv) + test_n] # test features
		test_l = lb_e[(test_n*cv):(test_n*cv) + test_n] # test labels

		feat = feat_e[:]
		feat[(test_n*cv):(test_n*cv) + test_n] = [] # train features
		lb = lb_e[:]
		lb[(test_n*cv):(test_n*cv) + test_n] = [] # train labels
		# print('lb size', len(lb))

		N = N_e - test_n # size of train chunks

		w = [1./dim for _ in range(dim)]
		b = -1.

		c = 0.2 # penalty of misclassification
		lr = 0.0005 # learning rate eta

		# train
		for k in range(50):
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
			w_len = sum(list(map(lambda x: x*x, w)))
			cost = 0.5*w_len + c*sum(list(map(lambda x: max(0, 1-x), margin)))
			# print('iteration', k,'accuracy:', acc, 'cost:', cost)

		margin_test = [test_l[j]*(dot(test_f[j],w)+b) for j in range(test_n)]
		temp = sum([(1. if margin_test[j] > 0 else 0.) for j in range(test_n)])/test_n
		acc_test.append(temp)

	# for acc in acc_test:
	# 	print('test accuracy', acc)

	print(sum(acc_test)/10)
	print(c)
	print(lr)

	# Result
	# 0.834666666667
	# 0.2
	# 0.0005
