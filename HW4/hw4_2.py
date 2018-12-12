import sys
from pyspark import SparkConf, SparkContext
import time

conf = SparkConf()
sc = SparkContext(conf=conf)
sc.setLogLevel('WARN') # skip terminal log to see output well

# entire features
feat_e = sc.textFile(sys.argv[1]).map(lambda s: s.split(','))\
								.map(lambda l: list(map(float,l)))
feat_e = feat_e.collect()

lb_e = sc.textFile(sys.argv[2]).map(lambda l: float(l)) # entire labels
lb_e = lb_e.collect()

N_e = len(feat_e) # the number of data
dim = len(feat_e[0]) # features size
acc_test = []
for cv in range(10):
	test_n = N_e/10 # size of test chunk
	N = N_e - test_n # size of train chunks

	test_f = feat_e[(test_n*cv):(test_n*cv) + test_n] # test features
	test_l = lb_e[(test_n*cv):(test_n*cv) + test_n] # test labels

	# ((data idx i, dimension idx j), feature[i][j]), remove if feature[i][j] is 0	
	test = sc.parallelize(range(test_n)) \
				.flatMap(lambda i: [((i,j), test_f[i][j]) for j in range(dim)]) \
				.filter(lambda l: l[1] != 0)

	feat = feat_e[:]
	feat[(test_n*cv):(test_n*cv) + test_n] = [] # train features
	lb = lb_e[:]
	lb[(test_n*cv):(test_n*cv) + test_n] = [] # train labels	

	# ((data idx i, dimension idx j), feature[i][j]), remove if feature[i][j] is 0
	train = sc.parallelize(range(N)) \
				.flatMap(lambda i: [((i,j), feat[i][j]) for j in range(dim)]) \
				.filter(lambda l: l[1] != 0)

	# print('count', train.count())

	w = [1./dim for _ in range(dim)]
	b = -1.

	c = 0.2 # penalty of misclassification
	lr = 0.0005 # learning rate eta	

	# train
	for k in range(50):
		cur_time = time.time()

		# (data idx i, lb[i]*(dot(feat[i],w)+b))
		margin = train.map(lambda l: (l[0][0], l[1]*w[l[0][1]])) \
					.reduceByKey(lambda v0, v1: v0 + v1) \
					.map(lambda l: (l[0], lb[l[0]]*(l[1]+b)))
					
		# (dimension index j, gradient)
		gd  = margin.filter(lambda l: l[1] < 1) \
				.flatMap(lambda l: [(j, -lb[l[0]]*feat[l[0]][j]) for j in range(dim)] \
																	+[(dim, -lb[l[0]])]) \
				.reduceByKey(lambda v0, v1: v0 + v1) \
				.map(lambda l: (l[0], w[l[0]] + c*l[1]) if l[0]<dim \
															else ((l[0], c*l[1]))) 
		# calculate new w and b
		w_n = gd.map(lambda l: (l[0], w[l[0]] - lr*l[1]) if l[0]<dim \
														else ((l[0], b - lr*l[1]))) \
				.sortByKey(True).map(lambda l: l[1]).collect()

		# update
		w = w_n[:dim]
		b = w_n[dim]

		acc = margin.map(lambda l: 1./N if l[1]>0 else 0.) \
					.reduce(lambda a, b: a+b)
		print('iteration', k, '%.3f seconds'%(time.time()-cur_time), 'accuracy:', acc)

	margin_test = test.map(lambda l: (l[0][0], l[1]*w[l[0][1]])) \
					.reduceByKey(lambda v0, v1: v0 + v1) \
					.map(lambda l: (l[0], test_l[l[0]]*(l[1]+b)))
	
	temp = margin_test.map(lambda l: 1./test_n if l[1]>0 else 0.) \
					.reduce(lambda a, b: a+b)
	print('%d fold test accuracy:'%cv, temp)
	acc_test.append(temp)

print(sum(acc_test)/10)
print(c)
print(lr)
