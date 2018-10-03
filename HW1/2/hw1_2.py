# using python 2.7

import sys
import operator

def id_to_n(id, prefix_char):
	# translate item id to integer
	prefix_index = prefix_char.index(id[:3])
	return prefix_index * 100000 + int(id[3:])

def n_to_id(n, prefix_char):
	# translate integer to item
	prefix_index = int(n)/100000
	return prefix_char[prefix_index] + str(n % 100000)

def tri_index(i, j, M):
	i = float(i)
	j = float(j)
	return int((i-1)*(M-i/2) + j - i - 1)

with open(sys.argv[1], 'r') as f:
	data = f.readlines()
	prefix_char = {} # fisrt 3 prefix character

###################################################
	# first pass
	# get the prefix characters
	for basket in data:
		items = basket[:-2].split(' ') # split by 'space', [:-2] for remove ' \n'
		for item in items:
			if not prefix_char.has_key(item[:3]):
				prefix_char[item[:3]] = 0
	prefix_char = list(prefix_char.keys()) # return prefix characters to list
	N = 100000 * len(prefix_char) # number of possible items

	item_counts = [0 for _ in range(N)]
	for basket in data:
		items = basket[:-2].split(' ') # split by 'space', [:-2] for remove ' \n'
		for item in items:
			item_counts[id_to_n(item, prefix_char)] += 1
###################################################
	# between the passes
	freq_table = [0 for _ in range(N)] # frequent-items table
	j = 0 # new numbering for frequent items
	for i in range(N):
		if item_counts[i] >= 200:
			j += 1
			freq_table[i] = j
	M = j # number of frequent items
###################################################
	# second pass
	# triangular matrix for storing frequent-items pair count
	tri_matrix = [0 for _ in range(M*(M-1)/2)]
	for basket in data:
		items = basket[:-2].split(' ') # split by 'space', [:-2] for remove ' \n'
		freq_items = [] # list for freqeunt items in the current basket

		# check which items are frequent
		for item in items:
			if item_counts[id_to_n(item, prefix_char)] >= 200:
				freq_items.append(item)
		# add one to each frequent-items pair 
		for i in range(len(freq_items)):
			for j in range(i+1, len(freq_items)):
				# new numbering (1 to M) for ith frequent item in the current basket
				u = freq_table[id_to_n(freq_items[i], prefix_char)]
				# new numbering (1 to M) for jth frequent item in the current basket
				v = freq_table[id_to_n(freq_items[j], prefix_char)]

				if u < v:
					tri_matrix[tri_index(u, v, M)] += 1	
				elif u > v:
					tri_matrix[tri_index(v, u, M)] += 1	
				else:
					pass

	freq_pairs = {}
	j = 0
	for i in range(len(tri_matrix)):
		if tri_matrix[i] >=200:
			j += 1

			breaker = False # break 'for loop' twice
			# find (u, v) index for triangular matrix
			for u in range(1, M+1):
				for v in range(u+1, M+1):
					if tri_index(u, v, M) == i:

						breaker = True
						break
				if breaker:
					break
			if not breaker:
				print('cannot find (u, v) pair')

			# get original numbering from (1 to M) index		
			s = freq_table.index(u)
			v = freq_table.index(v)

			freq_pairs[(n_to_id(s, prefix_char), n_to_id(v, prefix_char))] = tri_matrix[i]

	L = j # number of frequent pairs

	sorted_pairs = sorted(freq_pairs.items(), key=operator.itemgetter(1))
	sorted_pairs.reverse()
	
	print('Problem 2 output -----------------')
	print(str(M))
	print(str(L))
	for pair in sorted_pairs[:10]:
		print(pair[0][0]+ '\t' +pair[0][1]+ '\t' +str(pair[1]))
	print('----------------------------------')