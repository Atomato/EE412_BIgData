import sys
import re

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
			prefix_index = prefix_char.index(item[:3])

			# translate item id to integer
			item_number = prefix_index * 100000 + int(item[3:])
			item_counts[item_number] += 1
###################################################
	# between the passes
	

	print(item[3:])
	print(prefix_char)
	print(len(prefix_char))