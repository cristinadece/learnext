#!/usr/local/bin/python

'''
Created on Jan 23, 2013

@author: cris
'''

from TrajectoryUtils import *

trajectories = open("./input/Trajectories-FIRENZE-NEW.tsv", 'r')
pois_info = open("./input/Firenze-PoIs-NEW", 'r')
categ_pois = open("./input/Firenze-Cats", 'r')
training_ids = open("./svm-features/Firenze-training-ids", 'r')
test_ids = open("./svm-features/Firenze-test-ids", 'r')
ross_map = open("./ecir-data/ecir-adjacency-list-FI", 'w')

#categs -  dictionary POI - LIST of CATS

def load_freq():
    
    frequencies = {}
    training_session_ids = set()
    
    load_categ_pois(categ_pois)
    load_info_pois(pois_info)
    load_trajectories(trajectories)
    
    
    for line in training_ids:
        session_id = int(line.strip())
        training_session_ids.add(session_id)
        
    #print training_session_ids
    for session_id in training_session_ids:
        session = sessions[session_id]
        session_pois = session.get_pois()
        #print[poi.get_id() for poi in session_pois]
        for i, poi in enumerate(session_pois[:-1]):
            poi_id = poi.get_id()
            
            if poi_id not in frequencies:
                frequencies[poi_id] = {}
            current_poi = frequencies[poi_id]
          
            next_poi_id = session_pois[i+1].get_id()
            
            if next_poi_id in current_poi:
                current_poi[next_poi_id] += 1
            else:
                current_poi[next_poi_id] = 1

    print frequencies
            
    return frequencies

if __name__ == '__main__':
    
    frequencies_training = load_freq()
    print categs
    
    for start_node, stop_dict in frequencies_training.iteritems():
        
        total_freq_start = 0
        total_cats_start = 0
        
        for stop_node, freq in stop_dict.iteritems():
            total_freq_start += freq
            start_cats = categs.get(start_node, [])
            stop_cats = categs.get(stop_node, [])
            if start_cats == [] or stop_cats == []:
                common_cats = []
            else:
                common_cats = set(categs[start_node]).intersection(set(categs[stop_node]))
            total_cats_start += len(common_cats)
        
        total_start = total_cats_start + total_freq_start
        
        for stop_node, freq in stop_dict.iteritems():
            start_cats = categs.get(start_node, [])
            stop_cats = categs.get(stop_node, [])
            if start_cats == [] or stop_cats == []:
                common_cats = []
            else:
                common_cats = set(categs[start_node]).intersection(set(categs[stop_node]))
            s = ''
            s += start_node + "\t"
            s += stop_node + "\t"
            s += str((freq + len(common_cats)) / float(total_start)) + "\n"
            ross_map.write(s) 
            
    ross_map.close()
    
