#!/usr/bin/python

import sys

input_file = open(sys.argv[1], 'r')
iteration = 1
inverse_rank = float(0)
qid = ''

global_counter = 0
global_mmr = 0

line = input_file.readline()
qid = line.strip().split(' ')[1]
global_counter += 1
while (line != ''):
	line_fields = line.strip().split(' ')
	if (line_fields[1] == qid):
		if (line_fields[0] != '0'):
			inverse_rank = float(1) / iteration
		iteration += 1	
	else:
		qid = line_fields[1]
		global_mmr += inverse_rank
		global_counter += 1
		if (line_fields[0] != '0'):
			inverse_rank = 1
		else:
			inverse_rank = 0
		iteration = 2
	line = input_file.readline()
global_mmr += inverse_rank
print "MMR: " + str((global_mmr / global_counter))
