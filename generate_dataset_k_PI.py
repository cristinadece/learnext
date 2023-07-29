#!/usr/local/bin/python

'''
Created on Jan 3, 2013

@author: cris
'''

from TrajectoryUtils import *
import sys

trajectories = open("./input/Trajectories-PISA.tsv", 'r')
pois_info = open("./input/Pisa-PoIs", 'r')
categ_pois = open("./input/Pisa-Cats", 'r')
#training_ids = open("./svm-features/Pisa-training-ids", 'w')
#test_ids = open("./svm-features/Pisa-test-ids", 'w')
#training_file = open("./svm-features/Pisa-training-all-3neg", 'w')
#test_file = open("./svm-features/Pisa-test-all-3neg", 'w')

if __name__ == '__main__':
    
    print sys.argv
    k = int(sys.argv[1])
    # k is similar to n-1, the length of the session
    
    training_file = open("./svm-features/Pisa-training-all-max-"+str(k), 'w')
    test_file = open("./svm-features/Pisa-test-all-max-"+str(k), 'w')
    
    load_categ_pois(categ_pois)
    load_info_pois(pois_info)
    load_trajectories(trajectories)
    load_frequencies()

    # 80%
    dataset_fraction = 0.8
    n = 3

    session_ids = sessions.keys()    
    treshold = int(dataset_fraction * len(session_ids))
    training_set = set(session_ids[:treshold])
    test_set = set(session_ids[treshold:])
    
    '''
    for item in training_set:
        training_ids.write(str(item) + '\n')
    training_ids.close()
        
    for item in test_set:
        test_ids.write(str(item) + '\n')
    test_ids.close()
    
    print "Printed ids in separate files"
    '''
    
    training_matrix = []
    test_matrix = []
    s_f = []
    p_f = []
    count = 0
    for user in users.itervalues():
        for session in user.get_sessions():
            count += 1
            a = float(count*100)/len(sessions)
            print str("%.2f" %  a) + '%'
            #print session.get_id()
               
            if session.get_id() in training_set:
                feature_matrix = training_matrix
                neg_count = n
            elif session.get_id() in test_set:
                feature_matrix = test_matrix
                neg_count = -1
            else:
                continue
                
            
            if len(session.get_pois()) <= k + 1:
                next_poi = session.get_pois().pop()
            else:
                next_poi = session.get_pois().pop(k)  
                session.get_pois()[k:] =  []    
            
            s_f = compute_session_features(user, session)
            p_f = compute_poi_features(user, pois[next_poi.get_id()], session)
            s_fv = s_f.values()
            current_features = s_fv + p_f.values()
            feature_matrix.append([4, 'qid:' + str(session.get_id()).zfill(6)] + current_features)
            for negative_poi in generate_negative_pois(session, next_poi, neg_count):
                current_features = s_fv + compute_poi_features(user, pois[negative_poi], session).values()
                feature_matrix.append([0, 'qid:' + str(session.get_id()).zfill(6)] + current_features)

    print [(i+1, x) for i,x in enumerate(s_f.keys() + p_f.keys())]
                    
    #print [(i+1,f) for i,f in enumerate(feature_matrix[-1][2:])]
    means = None
    stds = None
    
    print 'Starting normalization and writing into files'
    
    for feature_matrix, output_file in ((training_matrix, training_file), (test_matrix, test_file)):
        normalized_matrix = numpy.array([row[2:] for row in feature_matrix], dtype='float')
        if means == None or stds == None:
            means = normalized_matrix.mean(axis=0)
            stds = normalized_matrix.std(axis=0)
        ### DIRTY TEMP FIX
        stds = [0.0000001 if x == 0 else x for x in stds]
        #print stds
        normalized_matrix -= means
        normalized_matrix /= stds
        
        for index, current_features in enumerate(normalized_matrix):
            output_file.write(' '.join(str(f) for f in feature_matrix[index][:2]) + ' ' + ' '.join(str(i+1) + ':' + str(f) for i, f in enumerate(current_features)) + '\n')
        output_file.close()
       
    print 'Finished writing into files. End process.'
            