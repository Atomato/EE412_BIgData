import sys
import re

def id_to_n(id, prefix_char):
	# translate item id to integer
	prefix_index = prefix_char.index(id[:3])
	return prefix_index * 100000 + int(item[3:])

def tri_index(i, j, M):
	return (i-1)*(M-i/2) + j - i - 1

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
	prefix_char = prefix_char.keys() # return prefix characters
	N = 100000 * len(prefix_char) # number of possible items

	item_counts = [0 for _ in range(N)]
	for basket in data:
		items = basket[:-2].split(' ') # split by 'space', [:-2] for remove ' \n'
		for item in items:
			# prefix_index = prefix_char.index(item[:3])

			# # translate item id to integer
			# item_number = prefix_index * 100000 + int(item[3:])
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
	# tri_matrix = [0 for _ in range(M*(M-1)/2)]
	# for basket in data:
	# 	items = basket[:-2].split(' ') # split by 'space', [:-2] for remove ' \n'
	# 	freq_items = [] # list for freqeunt items in the current basket
	# 	for item in items:
	# 		if 

	print('number of frequent items: ' + str(M))
	# item_counts.sort()
	# print(item_counts[-20:])
	print(prefix_char)
	print(len(prefix_char))