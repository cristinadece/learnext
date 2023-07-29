'''
Created on Jan 2, 2013

@author: cris

baseline su training e probability
C - 4 A - winner!!
C - 3 G
C - 2 B

'''

from TrajectoryUtils import *
training_ids = open("./svm-features/Pisa-training-ids", 'r')
trajectories = open("./input/Trajectories-PISA.tsv", 'r')
pois_info = open("./input/Pisa-PoIs", 'r')
categ_pois = open("./input/Pisa-Cats", 'r')
test_ids = open("./svm-features/Pisa-test-ids", 'r')
baseline = open("./baseline/Baseline-eval-Pisa-new-rare", 'w')

freq_pois_Pisa = ['P1', 'P109', 'P11', 'P18', 'PIPOIHPC1000000115', 'P16', 'P116', 'P101', 'P108', 'P107']

def load_frequencies():
    
    frequencies = {}
    frequencies_bigrams = {}
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
                
                
        if len(session_pois) > 2:
            for i, poi in enumerate(session_pois[:-2]):
                tupl = (poi.get_id(), session_pois[i+1].get_id())
                
                if tupl not in frequencies_bigrams:
                    frequencies_bigrams[tupl] = {}
                current_tupl = frequencies_bigrams[tupl]
                
                next_poi_id = session_pois[i+2].get_id()
                
                if next_poi_id in current_tupl:
                    current_tupl[next_poi_id] += 1
                else:
                    current_tupl[next_poi_id] = 1
    
                
    total = dict()
    for k, v in frequencies.iteritems():
        total[k] = 0 
        for k1, v1 in v.iteritems():
            total[k] += v1 
            
    for k, v in frequencies.iteritems():
        for k1, v1 in v.iteritems():
            v[k1] = float(v1) / total[k]


    total_bigrams = dict()
    for k, v in frequencies_bigrams.iteritems():
        total_bigrams[k] = 0 
        for k1, v1 in v.iteritems():
            total_bigrams[k] += v1 
            
    for k, v in frequencies_bigrams.iteritems():
        for k1, v1 in v.iteritems():
            v[k1] = float(v1) / total_bigrams[k]
            
    #print frequencies
    #print frequencies_bigrams
            
    return frequencies

if __name__ == '__main__':
    
    frequencies = load_frequencies()
     
    #print str(frequencies) + '\n'

    test_sessions_ids = set()
    for line in test_ids:
        session_id = int(line.strip())
        #print [poi.get_id() for poi in sessions[session_id].get_pois()]
        if sessions[session_id].get_pois()[-1].get_id() not in freq_pois_Pisa:
            test_sessions_ids.add(session_id)
    
    print test_sessions_ids
    # item before last and compare it with last
    for session_id in test_sessions_ids:
        #print[poi.get_id() for poi in sessions[session_id].get_pois()]
        last_poi = sessions[session_id].get_pois()[-2].get_id()
        #print last_poi
        if last_poi in frequencies:
            (freq_max, next_poi) = max((freq, poi_id) for poi_id, freq in frequencies[last_poi].iteritems())
            if (len(frequencies[last_poi]) > 1 and freq_max != 1):
                if next_poi == sessions[session_id].get_pois()[-1].get_id():
                    baseline.write(' '.join(['1', last_poi, next_poi, '\n']))
                    #print '1', last_poi, next_poi
                else:
                    #print '0', last_poi, next_poi
                    baseline.write(' '.join(['0', last_poi, next_poi, '\n']))
            elif (len(frequencies[last_poi]) == 1 and freq_max == 1):
                if next_poi == sessions[session_id].get_pois()[-1].get_id():
                    baseline.write(' '.join(['1', last_poi, next_poi, '\n']))
                    #print '1', last_poi, next_poi
                else:
                    #print '0', last_poi, next_poi
                    baseline.write(' '.join(['0', last_poi, next_poi, '\n']))
            else:
                baseline.write(' '.join(['null', last_poi, next_poi, '\n']))
        else:
            #print 'null', last_poi, '---'
            baseline.write(' '.join(['null', last_poi, '---', '\n']))
    
    baseline.close()

