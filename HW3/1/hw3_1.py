import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
sc.setLogLevel('WARN') # skip terminal log to see output well

lines = sc.textFile(sys.argv[1]) # read graph.txt
tuples = lines.map(lambda l: l.split('\t')) # split by tab, [src, dst]

# combine duplicated edges
tuples = tuples.map(lambda l: ((int(l[0]), int(l[1])), 0))\
			.reduceByKey(lambda v0, v1: v0+v1)\
			.map(lambda l: l[0])

triples = tuples.map(lambda l: (l[0], (1, [l[1]]))) # (source, (1, destination))

# calculate the degree of the source
# (source, (degree, [dst0, dst1, ...]))
triples = triples.reduceByKey(lambda v0, v1: (v0[0]+v1[0], v0[1]+v1[1]))

# transition matrix ((destination j, source i)), 1/degree of source (m_ij))
trans_mat = triples.flatMap(lambda l: [((l[0],l[1][1][i]), 1./l[1][0])\
								for i in range(len(l[1][1]))])

v = [1./1000 for _ in range(1000)] # initial vector

for _ in range(50):
	mat_mul = trans_mat.map(lambda l: (l[0][1], l[1]*v[l[0][0]-1])) # (i, m_ij*v_j)

	# sum all the value associated with key i (destination)
	v = mat_mul.reduceByKey(lambda v0, v1: v0 + v1)\
			.map(lambda l: l[1])\
			.collect()

page_rank = sc.parallelize([(v[i], i) for i in range(len(v))]) # (score, page id)
page_rank = page_rank.sortByKey(False) # sort by PageRank scores in descending order

for line in page_rank.take(10):
	print(str(line[1]) + '\t' + str(line[0]))

sc.stop()					