import re
import sys
from pyspark import SparkConf, SparkContext

def make_pseudo_friends(t):
	# make possible friend pairs from a friends list of each user
	friends = t[1] # friends list -> [friends]
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
sc.setLogLevel('WARN')

lines = sc.textFile(sys.argv[1]) # read data
tuples = lines.map(lambda l: l.split('\t')) # split by tab
tuples = tuples.map(lambda l: (l[0], l[1].split(','))) # map to (user, [friends])

# make pairs of actual friends
real_friends = tuples.flatMap(lambda l: [[l[0], l[1][i]] for i in range(len(l[1]))])
# formatting like -> ((user1, user2), (0, True))
# True means this pair is actual friends
real_friends = real_friends.map(lambda l: ((l[0], l[1]), (0, True)) if l[0]<l[1] \
					else ((l[1], l[0]), (0, True)))
# remove overlapped actual friends by reduce 
real_friends = real_friends.reduceByKey(lambda b1, b2: (b1[0] + b2[0], b1[1] or b2[1]))

# make possible friend pairs
# formatting like -> ((user1, user2), (1, False))
# 1 (fist value) means count of mutual friends
# False (second value) means this pair may not be actual friends
pseudo_friends = tuples.flatMap(make_pseudo_friends)
# union with real friends RDD, and reduce
# add up count of mutual friends, and or operation for boolean
# filter for excluding real friends
pseudo_friends = pseudo_friends.union(real_friends)\
					.reduceByKey(lambda b1, b2: (b1[0] + b2[0], b1[1] or b2[1]))\
					.filter(lambda l: l[1][1] is False)
					# .map(lambda l: l[0][0]+'\t'+l[0][1]+'\t'+str(l[1][0]))

					# sort by second user in ascending order
ordered_output = pseudo_friends.map(lambda l: (int(l[0][1]), (int(l[0][0]), l[1][0])))\
					.sortByKey(True)					
					# sort by first user in ascending order
ordered_output = ordered_output.map(lambda l: (l[1][0], (l[0], l[1][1])))\
					.sortByKey(True)
					# sort by number of mutual friends in descending order
ordered_output = ordered_output.map(lambda l: (l[1][1], (l[0], l[1][0])))\
					.sortByKey(False)
					# formatting like -> ((1st user, 2nd user), counts)
ordered_output = ordered_output.map(lambda l:(l[1], l[0]))

					# get the top-10 pairs
ordered_output = sc.parallelize(ordered_output.take(10))\
					.map(lambda l: str(l[0][0])+'\t'+str(l[0][1])+'\t'+str(l[1]))
					# formatting like <User><TAB><User><TAB><Count>

# ordered_output.saveAsTextFile(sys.argv[2])
# print(pseudo_friends.collect())
print('Problem 1 output -----------------')
for s in ordered_output.collect():
	print(s)
print('----------------------------------')
sc.stop()