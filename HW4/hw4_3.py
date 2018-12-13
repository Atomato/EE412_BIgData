# python 2.7
import sys

with open(sys.argv[1], 'r') as f:
	stream = f.readlines()
	stream = list(map(int, stream)) # change to number
	N = len(stream) # size of stream and also it is window size
	# print(N, stream[-10:])
	
	k_list = sys.argv[2:] # list of 'k_i' 
	k_list = list(map(int, k_list)) # change to integer

	buckets = {} # key: end time, value: size
	sizes = {} # key: size, value: [end times]
	for i in range(N):
		# if new bit is 1
		if stream[i] == 1:			
			buckets[i] = 1
			if 1 in sizes:
				sizes[1].append(i) # append end time
			else:
				sizes[1] = [i]

			for size, times in sorted(sizes.items()):
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

			# print('buckets', buckets)

	for size, times in sorted(sizes.items()):
		print(size, times)
	# print('sizes', sizes[1], sizes[2], sizes[4], sizes[8], sizes[16], sizes[32], sizes[64], sizes[128], sizes[256])
	# print('buckets', buckets)
	for k in k_list:
		estimate = 0
		temp = 0
		for size, times in sorted(sizes.items()):
			break_flag = False
			for time in reversed(times):
				time_idx = 0
				if N-k < time:
					estimate += temp
					print('k', k, 'size', size, 'temp', temp, 'time', time, 'estimate', estimate, 'break flag', break_flag)
					temp = size
				elif time == N-k: # corner case
					estimate += temp + 1
					break_flag = True
					print('k', k, 'size', size, 'temp', temp, 'time', time, 'estimate', estimate, 'break flag', break_flag)
					break
				else:
					estimate += temp / 2 if temp > 1 else 1
					break_flag = True
					print('k', k, 'size', size, 'temp', temp, 'time', time, 'estimate', estimate, 'break flag', break_flag)
					break
			if break_flag:
				break
		print(int(estimate))