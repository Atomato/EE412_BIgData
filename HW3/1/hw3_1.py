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
# print(triples.take(2))

# calculate the degree of the source
# (source, (degree, [dst0, dst1, ...]))
triples = triples.reduceByKey(lambda v0, v1: (v0[0]+v1[0], v0[1]+v1[1]))
# triples = triples.filter(lambda l: l[0] == u'994')
# print(triples.collect())

# transition matrix ((destination j, source i)), 1/degree of source (m_ij))
trans_mat = triples.flatMap(lambda l: [((l[0],l[1][1][i]), 1./l[1][0])\
								for i in range(len(l[1][1]))])
# print(trans_mat.take(1))

v = [1./1000 for _ in range(1000)] # initial vector
mat_mul = trans_mat.map(lambda l: (l[0][1], l[1]*v[l[0][0]-1])) # (i, m_ij*v_j)
v = mat_mul.reduceByKey(lambda v0, v1: v0 + v1)\
		.map(lambda l: l[1])\
		.collect()
print(v[:10])

# 					# get the top-10 pairs
# ordered_output = sc.parallelize(ordered_output.take(10))\
# 					.map(lambda l: str(l[0][0])+'\t'+str(l[0][1]))
# 					# formatting like <PAGE_ID><TAB><SCORE>

# for s in ordered_output.collect():
# 	print(s)

sc.stop()					