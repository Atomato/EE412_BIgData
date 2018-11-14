import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
sc.setLogLevel('WARN') # skip terminal log to see output well

lines = sc.textFile(sys.argv[1]) # read graph.txt
# print(lines.take(1))
tuples = lines.map(lambda l: l.split('\t')) # split by tab, [src, dst]
# print(tuples.take(2))
triples = tuples.map(lambda l: (l[0],(1, l[1]))) # (source, (degree, destination))
# print(triples.take(2))
triples = triples.reduceByKey(lambda v1, v2: (v1[0] + v2[0], (v1[1], v2[1])))
print(triples.take(1))

# 					# get the top-10 pairs
# ordered_output = sc.parallelize(ordered_output.take(10))\
# 					.map(lambda l: str(l[0][0])+'\t'+str(l[0][1]))
# 					# formatting like <PAGE_ID><TAB><SCORE>

# for s in ordered_output.collect():
# 	print(s)

sc.stop()					