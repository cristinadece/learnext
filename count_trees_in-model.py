__author__ = 'cris'


'''
Created on Apr 18, 2013

@author: cris
'''

from BeautifulSoup import BeautifulSoup
import operator
import sys



def readFile(filename):

    #source = open("./large-datasets/Firenze-model-all-3neg-15L-005LR.txt", 'r')
    source = open(filename, 'r')

    soup = BeautifulSoup(source)
    trees = soup.findAll('tree')

    i = 0
    for tree in trees:
        i += 1

    print i



if __name__ == '__main__':

    filename = sys.argv[1]
    print filename
    readFile(filename)





