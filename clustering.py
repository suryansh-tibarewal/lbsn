import mcl_clustering
import numpy as np
import networkx as nx
from collections import defaultdict
from constants import BRIGHTKITE_DATASET, GOWALLA_DATASET , eventType
import pickle
from similarityMatrixGenerator import getInterestList
from similarity import getSimilarityMatrix
import numpy as np


def get_clusters(dataset_type):
    try:
        if dataset_type == 0:
            with open('clusters_BRIGHTKITE_DATASET.pickle', "rb") as f:
                clusters = pickle.load(f)
        else:
            with open('clusters_GOWALLA_DATASET.pickle', 'rb') as f:
                clusters = pickle.load(f)
        return clusters

    except:
        G = nx.Graph()
        L = [-1]
        G.clear()
        if dataset_type == 0:
            edgeList = open('Brightkite_edges_filter.txt', 'r')
        else:
            edgeList = open('Gowalla_edges_filter.txt', 'r')
        for edge in edgeList:
            edge_entry = edge.split()
            from_edge = int(edge_entry[0].strip())
            to_edge = int(edge_entry[1].strip())
            if from_edge not in L:
                G.add_node(from_edge)
                L.append(from_edge)
            if to_edge not in L:
                G.add_node(to_edge)
                L.append(to_edge)

                G.add_edge(from_edge,to_edge)
        edgeList.close()
        M , clusters = mcl_clustering.networkx_mcl(G)
        if dataset_type == 0:
            with open("clusters_BRIGHTKITE_DATASET.pickle", "wb") as f:
                pickle.dump(clusters, f)
        else:
            with open("clusters_GOWALLA_DATASET.pickle", "wb") as f:
                pickle.dump(clusters, f)
        return clusters


def Gauss(a):
    return 0.5


def get_optimal_cluster(clusters,dataset_type):
    groups = []
    ranking = []
    for cluster in clusters:
        if clusters[cluster] not in groups:
             groups.append(clusters[cluster])

	user_list = user_object.getUserListFromFile(BRIGHTKITE_DATASET,NEG_ONLY)
    intrest_list = getInterestList('interests.txt')
    event_interest_count = [0]*len(interest_list)
    for eventType in eventType:
        event_interest_count[interest_list.index(eventType)]+=1
    group_intrest_count = [0]*len(intrest_list)
    similarityMatrix = getSimilarityMatrix('similarityMatrix.txt')

    for group in groups:
        num = 0
        for user in group:
            pos = user_list[user]['interests_list']
            neg = user_list[user]['neg_interests_list']
            for p in pos:
                group_interest_count[interest_list.index(p)]+=1
            for n in neg:
                group_interest_count[interest_list.index(n)]-=1

        for i in range (1,len(intrest_list)):
            for j in range (1,len(interest_list)):
                num += similarityMatrix[i][j]*group_interest_count[i]*event_interest_count[j]

        val = num/len(group)*Gauss(len(group))

        ranking.append([val,group])
    ranking.sort()
    return ranking[:5]

clusters = get_clusters(BRIGHTKITE_DATASET)
get_optimal_cluster(clusters,BRIGHTKITE_DATASET)
