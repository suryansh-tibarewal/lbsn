from simulation import F
from constants import e_lat, e_lon, setTemp
from clustering import get_clusters, get_optimal_clusters
from constants import BRIGHTKITE_DATASET, GOWALLA_DATASET ,eventType , NEG_ONLY , mean,pos_interest_mul , neg_interest_mul

def execute(candidate_set, start_from_index = 0):
    # candidate_set will be a sorted list based on score with 1st value as the score itself
    # and second value as the list of members. You can check the code to generate this type
    # of list in clustering.py

    f =  open('cluster_execution_results.txt', 'w')
    f.close()
    setTemp(1)

    for i in range(start_from_index, len(candidate_set)):
        print "entry", i
        if len(candidate_set[i][1]) <10:
            continue
        F((e_lon, e_lat), candidate_set[i])
        file_str = ''
        file_str += ((str(candidate_set[i][0])) + '\n')
        file_str += (str(len(candidate_set[i][1])) + '\n')
        file_str += (str(candidate_set[i][1]) + '\n')
        #file_str += str(answer + '\n')
        print file_str
        f = open('cluster_execution_results_jacc.txt', 'a')
        f.write(file_str)
        f.close()

clusters = get_clusters(BRIGHTKITE_DATASET)
candidate_set = get_optimal_clusters(clusters)
execute(candidate_set)        