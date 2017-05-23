from collections import defaultdict

graph_object_list = defaultdict(list)

def initialize(dataset_type):
    global graph_object_list
    graph_object_list.clear()
    if dataset_type == 0:
        edgeList = open('Brightkite_edges_filter.txt', 'r')
    else:
        edgeList = open('Gowalla_edges_filter.txt', 'r')
    for edge in edgeList:
        edge_entry = edge.split()
        from_edge = int(edge_entry[0].strip())
        to_edge = int(edge_entry[1].strip())
        graph_object_list[from_edge].append(to_edge)
    edgeList.close()

def checkDirectedEdge(from_vertex, to_vertex):
    global graph_object_list
    if from_vertex in graph_object_list:
        to_vertex_list = graph_object_list[from_vertex]
        if to_vertex in to_vertex_list:
            return True
        else:
            return False
    else:
        return False

##1 and 0 now not True and False, is it used somewhere else?
def checkUnDirectedEdge(from_vertex, to_vertex):
    if checkDirectedEdge(from_vertex, to_vertex) or checkDirectedEdge(to_vertex, from_vertex):
        return True
    else:
        return False
