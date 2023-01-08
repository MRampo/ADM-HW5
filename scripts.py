import networkx as nx
import pandas as pd
import re
import numpy as np
from queue import Queue 



# Common functions


def findNHeroes(data: pd.DataFrame, N: int) -> pd.DataFrame:
    NHeroes = list(data.groupby(by="hero")
    .count()                                            #count number of repetition
    .sort_values(by="comic", ascending=False)           #Sort values by "comic"
    .head(N)                                            #get top N
    .reset_index()                                      #reset index
    .hero)                                              #get only the names of our heroes
    return NHeroes




# Functionality 1


def findNetworksHub(graph, typeG, degreeDist):
    if typeG == 1:

        #return a list with just the degree of the graph
        tempDegree = dict(graph.degree())

    #if graph of type 2
    if typeG == 2:
        #create a dictionary of the nosed in G2
        dic = dict(graph.nodes(data="type"))

        #we take only the degree for the comics
        tempDegree = dict(graph.degree([k for k, v in dic.items() if v == "comic"]))

    #select the threshold
    threshold = np.quantile(list(tempDegree.values()), 0.95)
    
    #Select nodes based on threshold
    nodes = [k for k, v in tempDegree.items() if v > threshold ]

    return nodes


def findNNodes(graph, typeG):
    #take the number of nodes
    numberNodes = len(graph)
    
    #if graph is of type 2
    if typeG == "2":
        
        #create a dictionary from the nodes of the graph
        dic = dict(graph.nodes(data="type"))

        #select all the nodes that are comics
        numberComic = len([k for k, v in dic.items() if v == "comic"])
        
        #select all the nodes that are heroes
        numberHero = len([k for k, v in dic.items() if v == "hero"])

        #put them in a tuple
        numberNodes = (numberComic, numberHero)
    return numberNodes


def findNCollaboration(graph, typeG):
    #If graph is of type 1
    if typeG == 1:

        #return a list with just the degree of the graph
        return list(graph.degree())

    #if graph is of type 2
    if typeG == 2:
        
        #select all the nodes that are comic and take the degree
        dic = dict(graph.nodes(data="type"))
        return list(graph.degree([k for k, v in dic.items() if v == "comic"]))




# Functionality 3


def writePath(prev, source, target):
    #create empty list
    myList = []

    #create boolean in case the path is not found
    notFound = True
    
    #place the target in the list
    myList += [target]

    #if the value is a NaN
    if prev[target] == np.nan:
        return "Path Not Found!"
    
    #while True
    while notFound:

        #add the last node found in reverse
        myList += [prev[myList[-1]]]

        #if last one inserted is the source
        if myList[-1] == source:

            #then i found a path
            notFound= False
    
    # reverse the list
    myList.reverse()
    return myList


def findShortestPath(graph, couple):
    #select the source and the target
    source = couple[0]
    target = couple[1]

    #create a set of nodes to see which one we will have already visited
    nodesNotVisited = set(graph.nodes())
    
    #Create dist dictionary with np.inf as values
    dist = {node:np.inf for node in nodesNotVisited}

    #Create prev dictioary with np.nan as values
    prev = {node:np.nan for node in nodesNotVisited}

    #inizialize source
    dist[source] = 0

    #select minimum value
    myMin = min(dist.values())

    #while it has still nodes not visited
    while nodesNotVisited:
        
        #take all the nodes with min values
        nodes = [x for x, y in dist.items() if y == myMin and x in nodesNotVisited]

        #iterate over the previosy obtained nodes
        for node in nodes:

            #remove the node
            nodesNotVisited.remove(node)

            #take a list of the neighbors node that has been removed from the list
            neighbors = list(graph.neighbors(node))

            #iterate over the neighbors
            for neighbor in neighbors:

                #if the neighbor is in the list
                if neighbor in nodesNotVisited:
                    #update the value of the distance
                    newDist = dist[node] + 1

                    #if the new value is less than the distance of it's neigbours
                    if newDist < dist[neighbor]:
                        #update values
                        dist[neighbor] = newDist
                        prev[neighbor] = node
                #if the neigbor is the target then i finished my search
                if neighbor == target:
                    #write and return the path
                    myPath = writePath(prev, source, target)
                    return myPath
        #increase myMin
        myMin = myMin+1
    
    #write the path at the end
    myPath = writePath(prev, source, target)
    return myPath




# Visualization 3 


def define_labels(graph, path):
    # Get the labels just for the nodes in the path 
    labels = {}    
    # Iterate over the graph nodes
    for node in graph.nodes():
        # If I pass a node in the path
        if node in path:
            # Set the label to the node name
            labels[node] = node
        else:
            # Else leave it empty
            labels[node] = ""
    return labels


def find_edges(path):
    # Find the edges that you go though in the path, and save them in in a list
    f3_edge = []
    # Iterate over path's nodes
    for x in range(len(path)):
        if x < len(path)-1:
            # Append the touples that rappresent the wanted edge
            f3_edge.append((path[x], path[x+1]))
            f3_edge.append((path[x+1], path[x]))
    return f3_edge




# Functionality 4


def bfs_unweighted(graph,source):
    Q = Queue() ## create a queue 
    graph_dict = nx.to_dict_of_dicts(graph)
    visited = {key: False for key in graph_dict.keys()} ## Inizialize a dictionary where each key is a node and the value is False

    Q.put((source,source)) ## put the source inside the queue
    visited[source] = True ## source in visited is True now
    bfs_edges = list() ## use a list to store the paths
    try:
        while Q: ## while the queue is not empty
            s,path = Q.get(0) # drop the first element of the queue


            if s != source:
                bfs_edges.append((path,s)) ## put this element inside the paths list

            for neighbor in graph_dict[s].keys(): ## for each neighbor od s
                if visited[neighbor] == False:
                    Q.put((neighbor,s)) ## put the neighbour into the queue
                    visited[neighbor] = True ## change neighbor in visited equal to True

    except:
        pass
    return bfs_edges

## Below there is the BFS algorithm considering the weights of the edges, the steps are the same, the only difference is that we also add the weight of the edge
## into the queue

def bfs_weighted(graph,source):

    Q = Queue()
    graph_dict = nx.to_dict_of_dicts(graph)
    visited = {key: False for key in graph_dict.keys()}

    Q.put((source,source,0))
    visited[source] = True
    bfs_edges = list()

    while Q.empty()==False:
            s,path,weight = Q.get(0)

            if isinstance(weight,dict):
                bfs_edges.append((path,s,weight['weight']))

            for neighbor,weight in graph_dict[s].items():
                if visited[neighbor] == False:
                    Q.put((neighbor,s,weight))
                    visited[neighbor] = True


    return bfs_edges




# Functionality 5


def edge_to_remove(graph):

  #G_dict = nx.get_edge_attributes(graph, "weight")
  G_dict = nx.edge_betweenness_centrality(graph,weight ="weight", normalized=True)

  # extract the edge with highest edge betweenness centrality score
  edge, value = sorted(G_dict.items(), key=lambda item: item[1], reverse = True)[0]

  return edge


def edge_to_remove2(graph):

  #G_dict = nx.get_edge_attributes(graph, "weight")
  G_dict = nx.edge_betweenness_centrality(graph,weight ="weight", normalized=True)

  # extract the edge with highest edge betweenness centrality score
  edges = sorted(G_dict.items(), key=lambda item: item[1], reverse = True)
  edge, maxVal = sorted(G_dict.items(), key=lambda item: item[1], reverse = True)[0]
  return edges, maxVal


def girvan_newman(graph, n):
        # find the connected components
        sg = nx.connected_components(graph)

        # find the number of connected components
        sg_count = nx.number_connected_components(graph)

        #counter for the minimum number of edged needed to be cut to create a community
        count_edges = 0

        #while we have less than n community, we will keep on removing the edges
        while(sg_count < n):
            #select the edges to remove
            edges, maxVal = edge_to_remove2(graph)
            edges = [edge for edge, val in edges if val == maxVal]

            for edge in edges:
                #increase the counter
                count_edges += 1
                #remove the edge
                graph.remove_edge(edge[0], edge[1])

                #update the connected components
                sg = nx.connected_components(graph)

                #Uptdate the number of connected components
                sg_count = nx.number_connected_components(graph)

                if sg_count == n:
                    break
        
        return sg, count_edges, graph