'''
Created on Jan 9, 2013

@author: cris
'''

from TrajectoryUtils import *

training_ids = open("./svm-features/Rome-test-ids", 'r')
trajectories = open("./input/Trajectories-ROME.tsv", 'r')
pois_info = open("./input/Rome-PoIs", 'r')
categ_pois = open("./input/Rome-Cats", 'r')
where_next = open("./ecir-data/ecir-test-traj-RM", 'w')

def load_dictionaries():
    load_categ_pois(categ_pois)
    load_info_pois(pois_info)
    load_trajectories(trajectories)

if __name__ == '__main__':
    load_dictionaries()
    training_sessions_ids = set()
    for line in training_ids:
        session_id = int(line.strip())
        training_sessions_ids.add(session_id)
    print len(training_sessions_ids)
    
    counter = 0
    for session_id in training_sessions_ids:
        session = sessions[session_id]
        line = ''
        for u in users.itervalues():
            for s in u.get_sessions():
                if s.get_id() == session_id:
                    user_id = u.get_id()
	line = user_id + '\t'
        for visited_poi in session.get_pois():
	    line += visited_poi.get_id() + ';'
        where_next.write(line + '\n')
	counter += 1
    where_next.close()
