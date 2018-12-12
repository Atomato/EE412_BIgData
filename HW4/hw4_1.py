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
	feat = f.readlines() # features
	feat = list(map(lambda s: s.split(','),feat)) # split by comma
	feat = list(map(lambda l: list(map(float,l)),feat)) # change to number
	N = len(feat) # the number of data
	dim = len(feat[0]) # features size

	lb = l.readlines() # labels
	lb = list(map(float, lb)) # change to number

	# temp = sum([sum(feat[j]) for j in range(N)])/(N*len(feat[0]))
	# print('initail data', temp) # initail data distribution

	# temp = list(map(lambda x: (x + 1)/2., lb))
	# print('initail label', sum(temp)/N) # initail label distribution

	# print('len feat', len(feat[0]))
	# print('feat[0]', feat[0])
	# print('len label', len(lb))
	# print('label[:10]', lb[:10])
	# print('data num', N)

	w = [1./dim for _ in range(dim)]
	b = -1.

	c = 0.2 # penalty of misclassification
	lr = 0.0005 # learning rate eta



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
		w_len = sum(list(map(lambda x: x*x, w)))
		cost = 0.5*w_len + c*sum(list(map(lambda x: max(0, 1-x), margin)))
		print('accuracy:', acc, 'cost:', cost)	