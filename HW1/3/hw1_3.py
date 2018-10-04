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
	number_to_id = {}
	for i in range(len(data)):
		item = data[i] # for each article
		article_id = []
		for j in range(len(item)):
			# if first meet 'space'
			if item[j] == ' ':
				data[i] = data[i][j+1:] # exclude article id
				# id_to_number[''.join(article_id)] = i # article id to number
				number_to_id[i] = ''.join(article_id) # number to article id
				break
			# if not yet meet 'space'
			article_id.append(item[j])

	data = list(map(lambda d: d.lower(), data))
	# print(data[0])

	articles = list(map(lambda d: re.split(r'\s+', re.sub(r'[^a-z ]+', '', d)), data))
	# print(articles[0])

	# considering a shingle unit as an alphabetic character within a word (Case 1-A)
	# articles-shingle pairs table
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
	c = shingle_to_int('zzz') # the number of rows in shingle-set matrix as in Fig 3.4
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
	# get minhash signatures

	# signature matrix
	# first index is for article number, second index for signature values
	sig_table = [[c for _ in range(n)] for _ in range(len(articles))]

	# for each article
	for i in range(len(articles)):
		for j in range(n):
			# get the 'j'th signature value
			for shingle in shingles_set[i]:
				sig_table[i][j] = min((a[j]*shingle + b[j])%c, sig_table[i][j])
###################################################
	# find candidate pairs
	candidate_pairs = {}
	for i in range(bands):
		for j in range(len(articles)):
			for k in range(j+1, len(articles)):
				if sig_table[j][i*bands : i*bands+r] == sig_table[k][i*bands : i*bands+r]:
					candidate_pairs[(j, k)] = 0 # 0 has no meaning
###################################################
	# exmaine candidate pair by signature
	similar_pairs = {}
	for pair in candidate_pairs:
		similarity = 0.
		# for every signature value
		for i in range(n):
			if sig_table[pair[0]][i] == sig_table[pair[1]][i]:
				similarity += 1/float(n)
		# threshold is 0.9
		if similarity >= 0.9:
			similar_pairs[pair] = similarity

	sorted_pairs = sorted(list(similar_pairs.items()), key=operator.itemgetter(1))
	sorted_pairs.reverse()

	print('Problem 3 output -----------------')
	for pair in sorted_pairs:
		print(number_to_id[pair[0][0]] + '\t' + number_to_id[pair[0][1]] + \
					'\t' + str(pair[1]))
	print('----------------------------------')

stop = timeit.default_timer()

print('Run Time: ' + str(stop - start))