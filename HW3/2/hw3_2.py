import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
sc.setLogLevel('WARN') # skip terminal log to see output well

lines = sc.textFile(sys.argv[1]) # read graph.txt
tuples = lines.map(lambda l: l.split('\t')) # split by tab, [src, dst]

# combine duplicated edges and make link matrix (source i, destination j)
link_mat = tuples.map(lambda l: ((int(l[0]), int(l[1])), 0))\
			.reduceByKey(lambda v0, v1: v0+v1)\
			.map(lambda l: l[0])

h = [1. for _ in range(1000)] # initial Hubbiness

# zero vector for matrix multiplication (id, 0)
zero_vec = sc.parallelize([(i+1, 0.) for i in range(1000)])


for _ in range(50):
	# L^T * h = h^T * L -> (j, h_i)
	trans_mat_mul = link_mat.map(lambda l: (l[1], h[l[0]-1]))

	# sum all the value associated with key destination j (id, score)
	trans_mat_mul = trans_mat_mul.union(zero_vec).reduceByKey(lambda v0, v1: v0 + v1)

	# scaling factor for making largest component to be 1
	max_val = trans_mat_mul.map(lambda l: (l[1], l[0])).sortByKey(False)\
					.map(lambda l: l[0]).first()

	# make Authority vector by scaling
	a = trans_mat_mul.map(lambda l: (l[0], float(l[1])/max_val))\
				.sortByKey(True).map(lambda l: l[1]).collect()

	# L * a -> (i, a_j)
	mat_mul = link_mat.map(lambda l: (l[0], a[l[1]-1]))

	# sum all the value associated with key source i (id, score)
	mat_mul = mat_mul.union(zero_vec).reduceByKey(lambda v0, v1: v0 + v1)

	# scaling factor for making largest component to be 1
	max_val = mat_mul.map(lambda l: (l[1], l[0])).sortByKey(False)\
					.map(lambda l: l[0]).first()

	# make Hubbiness vector by scaling
	h = mat_mul.map(lambda l: (l[0], float(l[1])/max_val))\
				.sortByKey(True).map(lambda l: l[1]).collect()						

hubbiness = sc.parallelize([(h[i], i+1) for i in range(len(h))]) # (score, page id)
hubbiness = hubbiness.sortByKey(False) # sort by Hubbiness scores in descending order
authority = sc.parallelize([(a[i], i+1) for i in range(len(a))]) # (score, page id)
authority = authority.sortByKey(False) # sort by Authority scores in descending order

for line in hubbiness.take(10):
	print(str(line[1]) + '\t' + str(line[0]))
for line in authority.take(10):
	print(str(line[1]) + '\t' + str(line[0]))
###################################################
# 840	1.0
# 155	0.949961862491
# 234	0.898664528897
# 389	0.863417110184
# 472	0.86328410925
# 444	0.822971666987
# 666	0.800713998283
# 499	0.796614557082
# 737	0.774687762264
# 137	0.771514867731
# 893	1.0
# 16	0.963557284963
# 799	0.951015816107
# 146	0.92467035862
# 473	0.89986619736
# 624	0.892219751777
# 533	0.883241330491
# 780	0.880035784338
# 494	0.874988461507
# 130	0.846546535184	
###################################################

sc.stop()					