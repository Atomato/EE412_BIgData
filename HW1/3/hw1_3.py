# using python 2.7

import sys
import re
import timeit
import operator
from random import *

def shingle_to_int(shingle):
	# hash shingle to number
	if len(shingle) is not 3:
		print('error: shingle length is not 3')
	chars = [c for c in shingle]
	ints = list(map(lambda c: ord(c) - ord('a'), chars)) # alphabet to integer
	return 26*26*ints[0] + 26*ints[1] + ints[2] # the number of alphabet type is 26

start = timeit.default_timer()

with open(sys.argv[1], 'r') as f:
	data = f.readlines()
###################################################
	# numbering each article id and exclude article id
	id_to_number = {}
	for i in range(len(data)):
		item = data[i] # for each article
		article_id = []
		for j in range(len(item)):
			# if first meet 'space'
			if item[j] == ' ':
				data[i] = data[i][j+1:] # exclude article id
				id_to_number[''.join(article_id)] = i # article id to number
				break
			# if not yet meet 'space'
			article_id.append(item[j])

	data = list(map(lambda d: d.lower(), data))
	# print(data[0])

	articles = list(map(lambda d: re.split(r'\s+', re.sub(r'[^a-z ]+', '', d)), data))
	# print(articles[0])

	# considering a shingle unit as an alphabetic character within a word (Case 1-A)
	# articles-shingle pairs set
	shingles_set = [[] for _ in range(len(articles))]
	for i in range(len(articles)):
		item = articles[i] # for each article
		for word in item:
			if len(word) >= 3:
				for j in range(len(word)-2):
					# hash 3-characters shingle 
					# and append it to ith article set
					shingles_set[i].append(shingle_to_int(word[j:j+3]))
###################################################
	# choose number of bands and number of rows r as mentioned in HW! document
	bands = 6
	r = 20
	n = bands*r # number of minhash signatures, n = br as mentioned in textbook 3.4.3

	# find c to be the smallest prime number larger than or equal to n
	c = n
	prime = False
	while True:
		for i in range(2, c):
			remainder = c % i
			if remainder == 0:
				c += 1
				break
			# end of for loop -> c is prime number
			if i == c-1:
				prime = True
		if prime:
			break

	# a and b for hash function (ax + b)%c
	a = [randint(1, c-1) for _ in range(n)]
	b = [randint(1, c-1) for _ in range(n)]
###################################################
	

	print(shingles_set[1])
	print('c: ' + str(c))
	print('a: ' + str(a))
	# for pair in sorted(list(id_to_number.items()), key=operator.itemgetter(1))[:10]:
	# 	print(pair)

	# print(len(id_to_number))



stop = timeit.default_timer()

print('Run Time: ' + str(stop - start))