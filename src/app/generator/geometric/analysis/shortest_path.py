from  ..graph.SSTGraph import SSTGraph
from  ..graph.STGraph import STGraph
from ..math.Statistics import Statistics

#Shortest path stability algorithms used in SSDBM Submission

#object SSTLCPS {

'''
def jaccardIndex(a, b):
    #print('a',a,'b',b)
    intersection = a.intersection(b)
    union = a.union(b)
    if not union or len(union) == 0: 
        return 1.0
    else:
        return len(intersection) / len(union) 


def walk(temporalNetwork, srcId, start=0, end=len(temporalNetwork)):
    delta, path = {srcId: 0.0},{srcId: [srcId]}
    for time in range(start,end):
        g = temporalNetwork.get(time)
        for e in g.edges:
            source, target = e
            if source in delta:
                if delta.get(target) or float('inf')  > delta[source] + g[source][target]['weight']:
                    delta[target] = delta[source] + g[source][target]['weight']
                    path[target] = path[source] + [target]

    return (delta, path)
'''

def walk(tnet, srcId, start=0, end=len(tnet) ):
    delta, path = {srcId: 0.0}, {srcId: [srcId]}
    for time in range(start,end):
        graph = tnet.get(time)
        for e in graph.edges:
            source, target = e
            if source in delta:
                if delta.get(target) or float('inf')  > delta[source] + weight:
                    delta[target] = delta[source] + weight
                    path[target] = path[source] + [target]

    return (delta, path)

class StaticNetwork:
    def __init__(self):
        self.nodes = set()
        self.edges = dict()
    def addEdge(self, edge, weight=1):
        e = frozenset(edge)
        self.nodes |= e
        self.edges[e] = weight
    def addNode(self, node):
        self.nodes.add(node)
    

class TemporalNetwork:
    def __init__(self):
        self.snapshots = []
    def get(self, index=0):
        return self.snapshots[index]
    def add(self, graph):
        self.snapshots.append(graph)
    def __len__(self):
        return len(self.snapshots)

"""
Generators:
Uniform Network
Guassian Network

Power Law Network
-------------------------------------------------------------
import numpy as np

def power_law(k_min, k_max, y, gamma):
    return ((k_max**(-gamma+1) - k_min**(-gamma+1))*y  + k_min**(-gamma+1.0))**(1.0/(-gamma + 1.0))

nodes = 1000
#scale_free_distribution = np.zeros(nodes, float)
scale_free_distribution = np.zeros(nodes, int)
k_min = 1.0
k_max = 100*k_min
gamma = 3.0

for n in range(nodes):
    scale_free_distribution[n] = power_law(k_min, k_max,np.random.uniform(0,1), gamma) 

def generatePowerlaw(nodes, k_min, k_max, gamma):
    import random
    random.sample(range(0, nodes), degree)

import random
def assignEdges(degree_list):
    edges_list = []
    sorted_nodes = sorted(degree_list, reverse=True)
    count = len(sorted_nodes)
    valid_nodes = [i for i in range(count)]
    node = 0
    while (sum(sorted_nodes)):
        while(sorted_nodes[node]):
            random.range()

import random
degree_list = scale_free_distribution
sorted_nodes = sorted(degree_list, reverse=True)
#node_edges = [ node for node in range(count) for edge in range(sorted_nodes[node]) ] #works but hard to read
node_count = len(sorted_nodes)
node_ids = list(range(node_count))
node_edges = [ id for id in node_ids for degree in range(sorted_nodes[id]) ]
edge_list = []
for id in node_edges:
    print("id",id)
    degree = node_edges.count(id)
    current_node, node_edges = node_edges[:degree], node_edges[degree:]
    valid_nodes = set(node_edges)
    #print(degree, current_node)
    for id in current_node:
        print(len(current_node))
        other_id = random.choice(list(valid_nodes))
        print("removing",other_id, valid_nodes)
        valid_nodes.remove(other_id)
        edge_list.append( (id,other_id) )
        node_edges.remove(other_id)

#############################################################
#############################################################
#############################################################

import random
degree_list = scale_free_distribution
sorted_nodes = sorted(degree_list, reverse=True)
node_count = len(sorted_nodes)
node_ids = list(range(node_count))
node_edges = [ id for id in node_ids for degree in range(sorted_nodes[id]) ]
edge_list = []
for id in node_edges:
    print("id",id)
    degree = node_edges.count(id)
    node_edges = node_edges[degree:]
    valid_nodes = set(node_edges)
    neighbors = random.sample(list(valid_nodes),degree)
    edge_list += [(id, n) for n in neighbors]
    for n in neighbors:
        node_edges.remove(n)

#############################################################
#############################################################
#############################################################

import random
degree_list = scale_free_distribution
sorted_nodes = sorted(degree_list, reverse=True)
node_count = len(sorted_nodes)
node_ids = list(range(node_count))
node_edges = [ id for id in node_ids for degree in range(sorted_nodes[id]) ]
edge_list = set()
for id in node_edges:
    print("id",id)
    degree = node_edges.count(id)
    node_edges = node_edges[degree:]
    valid_nodes = set(node_edges)
    neighbors = random.sample(list(valid_nodes),degree)
    edge_list |= {(id, n) for n in neighbors}


#############################################################
#############################################################
#############################################################

import random
degree_list = scale_free_distribution
sorted_nodes = sorted(degree_list, reverse=True)
node_count = len(sorted_nodes)
node_ids = list(range(node_count))
node_edges = [ id for id in node_ids for degree in range(sorted_nodes[id]) ]
edge_list = set()
for id in node_edges:
    print("id",id)
    degree = node_edges.count(id)
    node_edges = node_edges[degree:]
    valid_nodes = set(node_edges)
    neighbors = random.sample(list(valid_nodes),degree)
    edge_list |= {tuple(sorted([id, n])) for n in neighbors}


#############################################################
#############################################################
#############################################################

import random
degree_list = scale_free_distribution
node_edges = [ id for id in range(len(degree_list)) for degree in range(degree_list[id]) ]
edge_list = set()
for id in node_edges:
    print("id",id)
    degree = node_edges.count(id)
    node_edges = node_edges[:degree] + node_edges[degree:]
    print(node_edges[degree])
    valid_nodes = set(node_edges)
    neighbors = random.sample(list(valid_nodes),degree)
    edge_list |= {tuple(sorted([id, n])) for n in neighbors}


#############################################################
#############################################################
#############################################################

import random
node_degrees = scale_free_distribution
node_ids = range(len(node_degrees))
edge_list = set()
for id in node_ids:
    print("id",id)
    degree = node_degrees[id]
    valid_nodes = set(node_ids) - {id}
    neighbors = random.sample(list(valid_nodes),degree)
    edge_list |= {tuple(sorted([id, n])) for n in neighbors}


#############################################################
#############################################################
#############################################################

import random
node_degrees = scale_free_distribution
node_ids = range(len(node_degrees))
edge_list = set()
for id in node_ids:
    print("id",id)
    degree = node_degrees[id]
    valid_nodes = set(node_ids) - {id}
    neighbors = random.choices(node_ids,weights=node_degrees,k=degree)
    edge_list |= {tuple(sorted([id, n])) for n in neighbors}


#############################################################
#############################################################
#############################################################
import numpy as np

def generate_powerlaw(scale_free_distribution):
    import random
    node_degrees = tuple(scale_free_distribution)
    node_ids = tuple(range(len(node_degrees)))
    edge_list = set()
    for id,degree in zip(node_ids, node_degrees):
        #print("id",id, "degree", degree)
        valid_nodes = node_ids[:id] + node_ids[id+1:]
        valid_degrees = node_degrees[:id] + node_degrees[id+1:]
        neighbors = random.choices(valid_nodes,weights=valid_degrees,k=degree)
        edge_list |= {tuple(sorted([id, n])) for n in neighbors}
    return edge_list

def draw_graph(edge_list):
    import networkx as nx
    import matplotlib.pyplot as plt
    g = nx.Graph(list(edge_list))
    nx.draw(g)
    plt.show()

def power_law(k_min, k_max, y, gamma):
    return ((k_max**(-gamma+1) - k_min**(-gamma+1))*y  + k_min**(-gamma+1.0))**(1.0/(-gamma + 1.0))


nodes = 100
#scale_free_distribution = np.zeros(nodes, float)
scale_free_distribution = np.zeros(nodes, int)
k_min = 1.0
k_max = 100*k_min
gamma = 3.0

for n in range(nodes):
    scale_free_distribution[n] = power_law(k_min, k_max,np.random.uniform(0,1), gamma) 

edge_list = generate_powerlaw(scale_free_distribution)
draw_graph(list(edge_list))

-------------------------------------------------------------



Evolution rules --> edge probabilities each snapshot

Temporal Network Generator Algorithm:
Parameters: 
node count, edge count, network type

Algorithm:
degreeList = IntArray[node count] filled with zeros
nodeList = []
Start with an initial node (id: 0) at position (0,0) add this node to nodelist
current node = node id
WHILE current node (id) < node count
    Randomly determine the max degree of current node, based on edge distribution of network type (i.e. Guassian, Power, Uniform)
    IF max degree > degreeList[current_node (id)]
        Randomly determine the radius reach of this node
        FOR EACH possible edge in degree count:
            IF current node in neighboorhod of a previous node(radius)
                Randomly select 
            ELSE
                Generate a new node (id)
                Randomly determine a distance (radius) between current node and new node
                Randomly determine a rotation value around current node for new node
                Calculate the spatial coordinate for new node
                Add new node to nodelist
                Randomly assign a probablity (0,1) for edge appearance
                Add new edge to edgelist

Ran

Walks & Paths

Community Assignments
IntraWalks
InterWalks

Centrality:



"""

def generateUniform():
    ""

def generateUniform():
    ""

def generateUniform():
    ""

