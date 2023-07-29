#!/usr/bin/python

import sys

input_file = open(sys.argv[1], 'r')
threshold = int(sys.argv[2])
iteration = 1
counter = 0
inverse_rank = float(0)
qid = ''

global_counter = 0
global_mmr = 0
global_pos_counter = 0

line = input_file.readline()
qid = line.strip().split(' ')[1]
global_counter += 1
while (line != ''):
	line_fields = line.strip().split(' ')
	if (line_fields[1] == qid):
		if (iteration <= threshold):
			if (line_fields[0] != '0'):
				#print line_fields[1]
				counter += 1
				inverse_rank = float(1) / iteration
		iteration += 1	
	else:
		qid = line_fields[1]
		global_pos_counter += counter
		global_mmr += inverse_rank
		global_counter += 1
		if (line_fields[0] != '0'):
			#print line_fields[1]
			counter = 1
			inverse_rank = 1
		else:
			counter = 0
			inverse_rank = 0
		iteration = 2
	line = input_file.readline()
global_pos_counter += counter
global_mmr += inverse_rank
print "One/Zero Test @" + str(threshold).zfill(2) + " (Ones, Zeroes, # TotalSessions, % Ones, MMR): " + str(global_pos_counter) + ", " + str(global_counter-global_pos_counter) + ", " + str(global_counter) + ", " + str((float(global_pos_counter) / global_counter) * 100) + ", " + str((global_mmr / global_counter))
