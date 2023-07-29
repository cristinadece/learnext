'''
Created on Apr 16, 2013

@author: cris
'''

file = open("./svm-features/Firenze-training-all-3neg", 'r')
output = open("./svm-features/Firenze-training-all-3neg-Rdata", 'w')

if __name__ == '__main__':
    for line in file:
        line_splitted = line.strip().split()
        sp = ""
        sp += line_splitted[0] + "\t"
        for val in line_splitted[2:]:
            val_splitted = val.strip().split(":")
            sp += val_splitted[1] + "\t"
        sp += "\n"
        output.write(sp)
    output.close()
        