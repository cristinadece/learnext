#!/usr/local/bin/python

'''
Created on Jan 3, 2013

@author: cris
'''

from TrajectoryUtils import *

trajectories = open("./input/Trajectories-ROME.tsv", 'r')
pois_info = open("./input/Rome-PoIs", 'r')
categ_pois = open("./input/Rome-Cats", 'r')
training_ids = open("./svm-features/Rome-training-ids-ROBERTO", 'w')
test_ids = open("./svm-features/Rome-test-ids-ROBERTO", 'w')
training_file = open("./svm-features/Rome-training-all-3neg-ROBERTO", 'w')
test_file = open("./svm-features/Rome-test-all-3neg-ROBERTO", 'w')

if __name__ == '__main__':
    
    # user related may be not relevant for test
    load_categ_pois(categ_pois)
    load_info_pois(pois_info)
    #print 'Example Poi', pois[908]
    load_trajectories(trajectories)
    load_frequencies()
    
    # 256 - Ponte_Vecchio
    #import operator
    #print min(((k, len(v)) for k, v in vpois.iteritems()), key = operator.itemgetter(1))
    
#    user_1 = users['29797746@N08']
#    poi_1 = pois[908]
#    session_1 = sessions[14139]
#    compute_poi_features(user_1, poi_1)
#    compute_session_features(user_1, session_1)

    # 80%
    dataset_fraction = 0.8
    n = -1

    session_ids = sessions.keys()    
    treshold = int(dataset_fraction * len(session_ids))
    training_set = set(session_ids[:treshold])
    #print training_set
    test_set = set(session_ids[treshold:])
    #print test_set
    

    for item in training_set:
        training_ids.write(str(item) + '\n')
    training_ids.close()
        
    for item in test_set:
        test_ids.write(str(item) + '\n')
    test_ids.close()
    
    print "Printed ids in separate files"
    
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
                
            #print '----'
            #print [poi.get_id() for poi in session.get_pois()]
            # the n-th element
            next_poi = session.get_pois().pop()  
            #print 'Positive poi ',  next_poi.get_id()
            #print [poi.get_id() for poi in session.get_pois()]
            s_f = compute_session_features(user, session)
            #print s_f
            p_f = compute_poi_features(user, pois[next_poi.get_id()], session)
            #print p_f
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
            

        
