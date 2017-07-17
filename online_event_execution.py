from simulation import F
from constants import e_lat, e_lon, setTemp

def execute(candidate_set, start_from_index = 0):
    # candidate_set will be a sorted list based on score with 1st value as the score itself
    # and second value as the list of members. You can check the code to generate this type
    # of list in clustering.py

    f =  open('cluster_execution_results.txt', 'w')
    f.close()
    setTemp(1)

    for i in range(start_from_index, len(candidate_set)):
        print i
        F((e_lon, e_lat), candidate)

        file_str = ''
        file_str += (str(candidate_set[i][0])) + '\n')
        file_str += (str(len(candidate_set[i][1])) + '\n')
        file_str += (str(candidate_set[i][1]) + '\n')
        f = open('cluster_execution_results.txt', 'a')
        f.write(file_str)
        f.close()
