# python 2.7
import sys

with open(sys.argv[1], 'r') as f:
	stream = f.readlines()
	stream = list(map(int, stream)) # change to number
	N = len(stream) # size of stream and also it is window size
	# print(N, stream[-10:])
	
	k_list = sys.argv[2:] # list of 'k_i' 
	k_list = list(map(int, k_list)) # change to integer

	sizes = {} # key: size, value: [end times]
	for i in range(N):
		# if new bit is 1
		if stream[i] == 1:			
			# buckets[i] = 1
			if 1 in sizes:
				sizes[1].append(i) # append end time
			else:
				sizes[1] = [i]

			for size, times in sorted(sizes.items()):
				# if there are 3 buckets of 'size'
				if len(times) == 3:
					# combine two leftmost buckets
					if 2 * size in sizes:
						sizes[2 * size].append(times[1])
					else:
						sizes[2 * size] = [times[1]]
					
					del sizes[size][:-1]

	# print buckets for debuging
	# for size, times in sorted(sizes.items()):
	# 	print(size, times)

	# for debuging
	# k_list = [N-2621313, N-2621314, N-2621315]

	for k in k_list:
		estimate = 0
		temp = 0 # previous bucket size
		for size, times in sorted(sizes.items()):
			break_flag = False
			for time in reversed(times):
				if N-k < time:
					estimate += temp
					# print(N-k, 'time', time, 'size', size, 'temp', temp, 'estimate', estimate, 'break flag', break_flag)
					temp = size
				elif time == N-k: # corner case
					estimate += temp + 1
					break_flag = True
					# print(N-k, 'time', time, 'size', size, 'temp', temp, 'estimate', estimate, 'break flag', break_flag)
					break
				else:
					estimate += 1 if temp == 1 else temp / 2
					break_flag = True
					# print(N-k, 'time', time, 'size', size, 'temp', temp, 'estimate', estimate, 'break flag', break_flag)
					break
			if break_flag:
				break				
		# if N-k < leftmost end time 
		if break_flag == False:
			estimate += 1 if temp == 1 else temp / 2
			break_flag = True
			# print(N-k, 'time', 0, 'size', 0, 'temp', temp, 'estimate', estimate, 'break flag', break_flag)			

		print(int(estimate))