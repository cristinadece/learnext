'''
Created on Apr 18, 2013

@author: cris
'''

from BeautifulSoup import BeautifulSoup
import operator

#source = open("./large-datasets/Pisa-model-all-3neg.txt", 'r')
source = open("./large-datasets/Firenze-model-all-3neg-15L-005LR.txt", 'r')
#source = open("./large-datasets/Rome-model-all-3neg-new-10L-001LR.txt", 'r')

def readFile():
    a = set()
    feature_matrix = []
    feature_occurences = {}
    soup = BeautifulSoup(source)
    trees = soup.findAll('tree')
    
    i = 0
    for tree in trees:
        tree_features = tree.findAll('splitfeatures')
        
        # build the matrix
        feature_array = [int(x) for x in tree_features[0].string.strip().split()]
        if i == 0:
            a = set(feature_array)
        else:
            a.update(set(feature_array))
        feature_matrix.append(feature_array)
        # map features with occurences
        for feature in feature_array:
            if feature in feature_occurences:
                feature_occurences[feature] += 1 
            else:
                feature_occurences[feature] = 1       
        i += 1 
        
    print i
    return [a, feature_matrix, feature_occurences]
        

if __name__ == '__main__':
    
    # Variables for Pisa: num leaves(pos) = 15; num trees = 70
    # Variables for Firenze: num leaves(pos) = 15; num trees = 111
    # Variables for Rome: num leaves = 10; num trees = 399
    
    
    aux = readFile()
    features = aux[0]
    #print features
    feature_matrix = aux[1] 
    #print feature_matrix
    feat_occ = aux[2]
    print "feature occurences"
    print feat_occ
    sorted_feat_occ = sorted(feat_occ.iteritems(), key = operator.itemgetter(1), reverse=True)
    print sorted_feat_occ
    
    feature_map  = {}
    for f in features:
        rank = 0
        for row in feature_matrix:
            if f in row:
                pos = row.index(f)
            else:
                pos = 15
            rank += pos
        feature_map[f] = float(rank)/111
        
    print feature_map
    sorted_feature_map = sorted(feature_map.iteritems(), key = operator.itemgetter(1))
    print sorted_feature_map
    
            
    

