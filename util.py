'''
Created on Jan 15, 2013

@author: cris
'''
file = open("./input/k-Firenze.txt", 'w')

if __name__ == '__main__':
    for x in range(1, 165):
        file.write(str(x) + "\n")
        print 'done'
    file.close()
