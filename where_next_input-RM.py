'''
Created on Jan 9, 2013

@author: cris
'''

from TrajectoryUtils import *

training_ids = open("./svm-features/Rome-training-ids", 'r')
test_ids = open("./svm-features/Rome-test-ids", 'r')
trajectories = open("./input/Trajectories-ROME.tsv", 'r')
pois_info = open("./input/Rome-PoIs", 'r')
categ_pois = open("./input/Rome-Cats", 'r')
where_next_training = open("./where-next/where-next-RM-training", 'w')
where_next_test_validation = open("./where-next/where-next-RM-test-validation", 'w')
where_next_test = open("./where-next/where-next-RM-test", 'w')


def load_dictionaries():
    load_categ_pois(categ_pois)
    load_info_pois(pois_info)
    load_trajectories(trajectories)

if __name__ == '__main__':
    load_dictionaries()
    
    # TRAINING generation
    training_sessions_ids = set()
    for line in training_ids:
        session_id = int(line.strip())
        #print [poi.get_id() for poi in sessions[session_id].get_pois()]
        training_sessions_ids.add(session_id)
    print len(training_sessions_ids)
    
    counter = 0
    for session_id in training_sessions_ids:
        session = sessions[session_id]
        line = ''
#        for u in users.itervalues():
#            for s in u.get_sessions():
#                if s.get_id() == session_id:
#                    user_id = u.get_id()
        for visited_poi in session.get_pois():
            lon = pois[visited_poi.get_id()].get_geo()[0]
            lat = pois[visited_poi.get_id()].get_geo()[1]
            start = visited_poi.get_start()
            #line = str(user_id) + ';' + str(lon) + ';' + str(lat) + ';' + str(start) + '\n'
            line = str(counter) + ';' + str(lon) + ';' + str(lat) + ';' + str(start) + '\n'
            where_next_training.write(line)
        counter += 1
    where_next_training.close()
    
    # TEST (up to n-1) and VALIDATION TEST (up to n) generation
    test_sessions_ids = set()
    for line in test_ids:
        session_id = int(line.strip())
        #print [poi.get_id() for poi in sessions[session_id].get_pois()]
        test_sessions_ids.add(session_id)
    print len(test_sessions_ids)
    
    counter = 0
    for session_id in test_sessions_ids:
        session = sessions[session_id]
        line = ''
#        for u in users.itervalues():
#            for s in u.get_sessions():
#                if s.get_id() == session_id:
#                    user_id = u.get_id()
        for visited_poi in session.get_pois()[:-1]:
            lon = pois[visited_poi.get_id()].get_geo()[0]
            lat = pois[visited_poi.get_id()].get_geo()[1]
            start = visited_poi.get_start()
            #line = str(user_id) + ';' + str(lon) + ';' + str(lat) + ';' + str(start) + '\n'
            line = str(counter) + ';' + str(lon) + ';' + str(lat) + ';' + str(start) + '\n'
            where_next_test.write(line)
            where_next_test_validation.write(line)
        lon_n = pois[session.get_pois()[-1].get_id()].get_geo()[0]
        lat_n = pois[session.get_pois()[-1].get_id()].get_geo()[1]
        start_n = session.get_pois()[-1].get_start()
        line_n = str(counter) + ';' + str(lon_n) + ';' + str(lat_n) + ';' + str(start_n) + '\n'
        where_next_test_validation.write(line_n)
        counter += 1
    where_next_test.close()
    where_next_test_validation.close()
