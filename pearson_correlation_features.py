'''
Created on May 7, 2013

@author: cris
'''
import numpy
from numpy import mean, dot
from numpy.linalg import norm
import networkx as nx

file = open("./svm-features/Firenze-training-all-3neg", 'r')
rdata = open("./svm-features/Firenze-training-all-3neg-RData-real-traj", 'w')

def correlation(x, y):
    cx = x - mean(x)
    cy = y - mean(y )
    return dot(cx, cy) / (norm(cx) * norm(cy))

def covariance(x, y):
    return

def load_graph():
    feature_distrib = []
    for line in file:
        line_splitted = line.strip().split()
        if int(line_splitted[0])==4:
            sp = []
            for val in line_splitted[2:]:
                val_splitted = val.strip().split(":")
                sp.append(val_splitted[1])
                rdata.write(val_splitted[1]+"\t")
            feature_distrib.append(sp)
            rdata.write("\n")
    mat =  numpy.array(feature_distrib, dtype='float')
    rdata.close()
    
    pearson = numpy.zeros(shape=(68,68))
    
    G = nx.Graph()
    
    with open("./svm-features/Pearson_correlation_FI", 'w') as output:
        for i in range(68):
            for j in range(68):
                if i != j :
                    c = pearson[i][j] = correlation(mat[:,i], mat[:,j])
                    if abs(c) > 0.9:
                        G.add_edge(i, j, c=c)
                        output.write(str(i) + "\t" + str(j) + "\t" + str(pearson[i][j]) + "\n")

    return G

def covariance_matrix():
    return
    
def main():
     G = load_graph()
     connected_subgraphs = nx.connected_component_subgraphs(G)
     for g in connected_subgraphs:
         print g.nodes() 
    
if __name__ == '__main__':
    main()