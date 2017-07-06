import mcl_clustering
import numpy as np
import networkx as nx
from collections import defaultdict
from constants import BRIGHTKITE_DATASET, GOWALLA_DATASET ,eventType , NEG_ONLY , mean,pos_interest_mul , neg_interest_mul
import pickle
from similarityMatrixGenerator import getInterestList
from similarity import getSimilarityMatrix
import numpy as np
import user_object


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
                pickle.dump(clusters, f,2)
        else:
            with open("clusters_GOWALLA_DATASET.pickle", "wb") as f:
                pickle.dump(clusters, f,2)

        ####### USERS pickle
        if dataset_type == 0:
            with open("clusters_BRIGHTKITE_DATASET_graph.pickle", "wb") as f:
                pickle.dump(G , f,2)
        else:
            with open("clusters_GOWALLA_DATASET_graph.pickle", "wb") as f:
                pickle.dump(G , f,2)
        return clusters


def gaussian(x):
    standard_dev = 2
    return np.exp(-np.power(x - mean, 2.) / (2 * np.power(standard_dev, 2.)))

def get_optimal_cluster(clusters,eventType):
    user_map = getusers()
    groups = get_cluster_groups(user_map,clusters)

    ranking = []
    user_list = user_object.getUserListFromFile(BRIGHTKITE_DATASET)
    interest_list = getInterestList('interests_list.txt')
    event_interest_count = [0]*len(interest_list)

    for eventType in eventType:
        event_interest_count[interest_list.index(eventType)]+=1

    similarityMatrix = getSimilarityMatrix('similarityMatrix.txt')

    for group in groups:
        group_interest_count = [0]*len(interest_list)
        num = 0
        for user in group:
            pos = user_list[user]['interests_list']
            neg = user_list[user]['neg_interests_list']
            for p in pos:
                group_interest_count[interest_list.index(p)]+=pos_interest_mul
            for n in neg:
                group_interest_count[interest_list.index(n)]-=neg_interest_mul

        # for index,inter in enumerate(group_interest_count):
        #     if(event_interest_count[index]>0):
        #         print (inter)
        for i in range (len(interest_list)):
            for j in range (len(interest_list)):
                num += similarityMatrix[i][j]*group_interest_count[i]*event_interest_count[j]

        val = (num*gaussian(len(group)))/len(group)

        ranking.append([val,group])
    ranking.sort(reverse=True)
    return ranking[:5]

def getusers():
    G = nx.Graph()
    with open('clusters_BRIGHTKITE_DATASET_graph.pickle', "rb") as f:
        G = pickle.load(f)
    S = []
    for user in G.nodes():
        S.append(user)
    return S

def get_cluster_groups(user_map,clusters):
    S = []
    for cluster in clusters:
        R=[]
        for member in clusters[cluster]:
            R.append(user_map[member])
        if R not in S:
            S.append(R)
    return S

clusters = get_clusters(BRIGHTKITE_DATASET)

S = []

# for cluster in clusters:
#     for user in clusters[cluster]:
#         if user not in S:
#             S.append(user)
# print (len(S))
#print (gaussian(19))

print(get_optimal_cluster(clusters,['Aquariums','Biking','Ceramics']))
