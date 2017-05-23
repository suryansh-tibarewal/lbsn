import mcl_clustering
import numpy as np
import networkx as nx
from collections import defaultdict
import pickle



def get_clusters(dataset_type):
    try:
        with open("clusters.pickle", "rb") as f:
            cluster = pickle.load(f)
        return cluster

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
        with open("clusters.pickle", "wb") as f:
            pickle.dump(clusters, f)
        return clusters
