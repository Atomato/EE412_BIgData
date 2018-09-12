import re
import sys
from pyspark import SparkConf, SparkContext

def make_pseudo_friends(t):
	friends = t[1]
	pairs = []
	for i in range(0, len(friends)):
		for j in range(i+1, len(friends)):
			if friends[i] < friends[j]:
				pairs.append(((friends[i], friends[j]), (1, False)))
			else:
				pairs.append(((friends[j], friends[i]), (1, False)))
	return pairs

conf = SparkConf()
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1])
tuples = lines.map(lambda l: l.split('\t'))
tuples = tuples.map(lambda l: (l[0], l[1].split(',')))

real_friends = tuples.flatMap(lambda l: [[l[0], l[1][i]] for i in range(len(l[1]))])
real_friends = real_friends.map(lambda l: ((l[0], l[1]), (0, True)) if l[0]<l[1] \
					else ((l[1], l[0]), (0, True)))
real_friends = real_friends.reduceByKey(lambda b1, b2: (b1[0] + b2[0], b1[1] or b2[1]))

pseudo_friends = tuples.flatMap(make_pseudo_friends)
pseudo_friends = pseudo_friends.union(real_friends)\
					.reduceByKey(lambda b1, b2: (b1[0] + b2[0], b1[1] or b2[1]))\
					.filter(lambda l: l[1][1] is False)\
					.map(lambda l: l[0][0]+'\t'+l[0][1]+'\t'+str(l[1][0]))

print(real_friends.collect())
for _ in range(3):
	print('\n')

print(pseudo_friends.collect())
for _ in range(3):
	print('\n')