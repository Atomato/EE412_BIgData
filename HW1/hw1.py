import re
import sys
from pyspark import SparkConf, SparkContext

def make_pair(t):
	freinds = t[1]
	pairs = []
	for i in range(0, len(freinds)):
		for j in range(i+1, len(freinds)):
			pairs.append([freinds[i], freinds[j]])
	return pairs

conf = SparkConf()
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1])

tuples = lines.map(lambda l: l.split('\t'))
tuples = tuples.map(lambda l: (l[0], l[1].split(',')))

f_tuples = tuples.flatMap(make_pair)

print(f_tuples.collect())
for _ in range(3):
	print('\n')
