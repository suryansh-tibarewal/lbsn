import mcl_clustering
import numpy as np
import networkx as nx
from collections import defaultdict
from constants import BRIGHTKITE_DATASET, GOWALLA_DATASET
import pickle



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


def get_optimal_cluster(clusters):
	return clusters[0]
