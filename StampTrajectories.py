__author__ = 'cris'


def load_trajectories(trajectories, trajectoriesOutput, exclude_single_poi=True):
    for line in trajectories:
        line_splitted = line.strip().split("\t")

        if len(line_splitted) <= 2 and exclude_single_poi:
            continue

        for point in line_splitted[1:]:
            point_info = point.strip().split(";")
            poi_id = point_info[0]
            trajectoriesOutput.write(poi_id + ' ')


        trajectoriesOutput.write('\n')

if __name__ == '__main__':

    path = "/Users/cris/Documents/workspace/turism/Turismo-LETOR/LearNext-Dataset/"

    trajectoriesPisa = open(path + "Pisa/Trajectories-PISA.tsv", 'r')
    trajectoriesPisaOutput = open(path + "Pisa/Trajectories-PISA-plain.tsv", 'w')
    load_trajectories(trajectoriesPisa, trajectoriesPisaOutput)
    trajectoriesPisa.close()

    trajectoriesFlorence = open(path + "Florence/Trajectories-FLORENCE.tsv", 'r')
    trajectoriesFlorenceOutput = open(path + "Florence/Trajectories-FLORENCE-plain.tsv", 'w')
    load_trajectories(trajectoriesFlorence, trajectoriesFlorenceOutput)
    trajectoriesFlorence.close()

    trajectoriesRome = open(path + "Rome/Trajectories-ROME.tsv", 'r')
    trajectoriesRomeOutput = open(path + "Rome/Trajectories-ROME-plain.tsv", 'w')
    load_trajectories(trajectoriesRome, trajectoriesRomeOutput)
    trajectoriesRome.close()
