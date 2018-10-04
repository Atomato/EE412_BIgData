# using python 2.7

import sys
import re
import timeit
import operator

start = timeit.default_timer()

with open(sys.argv[1], 'r') as f:
	data = f.readlines()

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

	print(articles[0])


	# for pair in sorted(list(id_to_number.items()), key=operator.itemgetter(1))[:10]:
	# 	print(pair)

	# print(len(id_to_number))



stop = timeit.default_timer()

print('Run Time: ' + str(stop - start))