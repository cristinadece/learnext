__author__ = 'cris'

"""


"""

from TrajectoryUtils import *

trajectories = open("./input/Trajectories-PISA.tsv", 'r')
pois_info = open("./input/Pisa-PoIs", 'r')
categ_pois = open("./input/Pisa-Cats", 'r')
training_trails = open("./input/Pisa-training-trails", 'w')
test_trails = open("./input/Pisa-test-trails", 'w')
test_trails_no_last = open("./input/Pisa-test-trails-no-last", 'w')


if __name__ == '__main__':

    load_categ_pois(categ_pois)
    load_info_pois(pois_info)
    load_trajectories(trajectories)

    # 80%
    dataset_fraction = 0.8
    session_ids = sessions.keys()
    treshold = int(dataset_fraction * len(session_ids))

    training_set = set(session_ids[:treshold])
    test_set = set(session_ids[treshold:])

    for item in training_set:
        for vpoi in sessions[item].get_pois():
          training_trails.write(vpoi.get_id() + ' ')
        training_trails.write('\n')
    training_trails.close()

    for item in test_set:
        for vpoi in sessions[item].get_pois():
          test_trails.write(vpoi.get_id() + ' ')
        test_trails.write('\n')
        for vpoi in sessions[item].get_pois()[:-1]:
          test_trails_no_last.write(vpoi.get_id() + ' ')
        test_trails_no_last.write('\n')

    test_trails.close()
    test_trails_no_last.close()