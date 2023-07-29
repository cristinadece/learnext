'''
Created on Jan 14, 2013

@author: cris
'''

from TrajectoryUtils import *


trajectories = open("./input/Trajectories-PISA.tsv", 'r')
pois_info = open("./input/Pisa-PoIs", 'r')
categ_pois = open("./input/Pisa-Cats", 'r')
#sessions_len = open("./large-datasets/Session-lengths", 'w')

#trajectories = open("./input/Trajectories-FIRENZE-NEW.tsv", 'r')
#pois_info = open("./input/Firenze-PoIs-NEW", 'r')
#categ_pois = open("./input/Firenze-Cats", 'r')
#sessions_len = open("./large-datasets/Session-lengths", 'w')

#trajectories = open("./input/Trajectories-ROME.tsv", 'r')
#pois_info = open("./input/Rome-PoIs", 'r')
#categ_pois = open("./input/Rome-Cats", 'r')
#sessions_len = open("./large-datasets/Session-lengths", 'w')
session_time = open("./large-datasets/Session-time-Pisa", 'w')


if __name__ == '__main__':
    load_categ_pois(categ_pois)
    load_info_pois(pois_info)
    #print 'Example Poi', pois[908]
    load_trajectories(trajectories)
    diff = 0;
    
    for i,s in enumerate(sessions.itervalues()):
        #sessions_len.write(str(len(s.get_pois()))+ '\n')
        diff = s.get_pois()[-1].get_stop() - s.get_pois()[0].get_start()
        print diff
        session_time.write(str(i) + '\t' + str(diff) + '\n')
        
    #sessions_len.close()
    session_time.close()
    
    for p in sessions[377].get_pois():
        print p
    
    print 'Max traj len Firenze', max([len(s.get_pois()) for s in sessions.itervalues()])