#!/usr/local/bin/python

'''
Created on Jan 25, 2013

@author: cris
'''

from TrajectoryUtils import *
import sys

trajectories = open("./input/Trajectories-PISA.tsv", 'r')
pois_info = open("./input/Pisa-PoIs", 'r')
categ_pois = open("./input/Pisa-Cats", 'r')
training_ids = open("./svm-features/Pisa-training-ids", 'r')
test_ids = open("./svm-features/Pisa-test-ids", 'r')
poi_distrib_file = open("./input/Pisa-poi-distribution", 'w')
#rare_poi_sessions = open("./svm-features/Rare-poi-session-ids-PI", 'w')
#freq_poi_sessions = open("./svm-features/Freq-poi-session-ids-PI", 'w')
test_file = open("./svm-features/Pisa-test-all-3neg", "r")
test_file_rare = open("./svm-features/Pisa-test-all-3neg-rare", "w")
test_file_freq = open("./svm-features/Pisa-test-all-3neg-freq", "w")

THRESHOLD = 100
freq_pois = {}
rare_pois ={}
freq_ses = []
rare_ses = []

def print_distrib_file():
    global freq_pois, rare_pois
    
    pois_in_training = set()
    # vpois id a dictionary with poiid and list of vpois, the freq is given by the len of the list
    for session_id in training_ids:
        for p in sessions[int(session_id)].get_pois():
            pois_in_training.add(p.get_id())
    
    for poi_id in pois_in_training:
        if len(vpois[poi_id]) >THRESHOLD:
            freq_pois[poi_id] = len(vpois[poi_id])
        else:
            rare_pois[poi_id] = len(vpois[poi_id])
        poi_distrib_file.write(poi_id + '\t' + str(len(vpois[poi_id])) + '\n')
    poi_distrib_file.close()

if __name__ == '__main__':
    
    load_categ_pois(categ_pois)
    load_info_pois(pois_info)
    load_trajectories(trajectories)
    
    print_distrib_file()
    
    print freq_pois
    print rare_pois
    
    for session_id in test_ids:
        if sessions[int(session_id)].get_pois()[-1].get_id() in freq_pois:
            #freq_poi_sessions.write(session_id)
            freq_ses.append(int(session_id))
        else:
            #rare_poi_sessions.write(session_id)
            rare_ses.append(int(session_id))
    
    #freq_poi_sessions.close()
    #rare_poi_sessions.close()
    
    for line in test_file:
        session_id = int(line.strip().split(" ")[1].split(":")[1])
        if session_id in rare_ses:
            test_file_rare.write(line)
        else:
            test_file_freq.write(line)
            
    test_file_freq.close()
    test_file_rare.close()
    