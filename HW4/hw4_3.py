# python 2.7
import sys

with open(sys.argv[1], 'r') as f:
	stream = f.readlines()
	stream = list(map(int, stream)) # change to number
	N = len(stream) # size of stream and also it is window size
	print(N, stream)
	
	M = len(sys.argv)-2
	# print(M)
	k_list = sys.argv[2:] # list of 'k_i' 
	# print(len(k_list))

	buckets = {} # key: end time, value: size
	sizes = {} # key: size, value: [end times]
	for i in range(N):
		if stream[i] == 1:			
			buckets[i] = 1
			if 1 in sizes:
				sizes[1].append(i) # append end time
			else:
				sizes[1] = [i]

			for size, times in sizes.items():
				# print('before', size, times)

				# if there are 3 buckets of 'size'
				if len(times) == 3:
					# combine two leftmost buckets
					buckets[times[1]] = 2 * size
					del buckets[times[0]]

					if 2 * size in sizes:
						sizes[2 * size].append(times[1])
					else:
						sizes[2 * size] = [times[1]]
					
					del sizes[size][:-1]

				# print('after', size, times)
			# print('buckets', buckets)