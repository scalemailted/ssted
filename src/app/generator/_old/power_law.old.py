from models.network import *
from generator.generator_utils import *


import numpy as np
import random
import networkx as nx
import os
import copy


#TEST
#tnet = TemporalNetwork()
#print(tnet)

"""
def powerlaw_edgelist(scale_free_distribution):
    node_degrees = tuple(scale_free_distribution)
    node_ids = tuple(range(len(node_degrees)))
    edge_list = set()
    for id,degree in zip(node_ids, node_degrees):
        valid_nodes = node_ids[:id] + node_ids[id+1:]
        valid_degrees = node_degrees[:id] + node_degrees[id+1:]
        neighbors = random.choices(valid_nodes,weights=valid_degrees,k=degree)
        edge_list |= {tuple(sorted([id, n])) for n in neighbors}
    return edge_list
"""

"""
#general function --> remove from this and import after refactoring
def generate_edges(node_degrees):
    edge_list = set()
    node_ids = tuple(range(len(node_degrees)))
    for id, degree in zip(node_ids, node_degrees):
        other_nodes = node_ids[:id] + node_ids[id+1:]
        other_degrees = node_degrees[:id] + node_degrees[id+1:]
        neighbors = random.choices(other_nodes,weights=other_degrees,k=degree)
        edge_list |= {tuple(sorted([id, n])) for n in neighbors}
    return edge_list

#tester function, not needed in this script
def draw_graph(edge_list):
    import matplotlib.pyplot as plt
    g = nx.Graph(list(edge_list))
    nx.draw(g)
    plt.show()

def powerlaw(k_min, k_max, y, gamma):
    return ((k_max**(-gamma+1) - k_min**(-gamma+1))*y  + k_min**(-gamma+1.0))**(1.0/(-gamma + 1.0))


def generate_degrees(nodes, k_min, k_max, gamma):
    degree_list = np.zeros(nodes, int)
    for n in range(nodes):
        degree_list[n] = powerlaw(nodes, k_min, k_max, y=np.random.uniform(0,1), gamma)
    return degree_list

def generate(nodes=100, k_min=1.0, k_max=100, gamma=3.0):
    degree_list = generate_degrees(nodes, k_min, k_max, gamma)
    edge_list = generate_edges(degree_list)
    return edge_list

"""

def powerlaw(k_min, k_max, y, gamma):
    y = np.random.uniform(0,1)
    return ((k_max**(-gamma+1) - k_min**(-gamma+1))*y  + k_min**(-gamma+1.0))**(1.0/(-gamma + 1.0))

def generate(nodes=100, k_min=1.0, k_max=100, gamma=3.0):
    degree_list = generate_degrees(powerlaw, nodes, k_min, k_max, gamma)
    edge_list = generate_edges(degree_list)
    return edge_list

"""
def generate_degrees(function, nodes=100, *args):
    degree_list = np.zeros(nodes, int)
    for n in range(nodes):
        degree_list[n] = function(nodes, *args) 
    return tuple(degree_list)
"""



"""
def generate_degreelist(nodes=100, k_min=1.0, k_max=100, gamma = 3.0):
    print("Generating Powerlaw Distribution")
    degree_list = np.zeros(nodes, int)
    for n in range(nodes):
        degree_list[n] = powerlaw(k_min, k_max, np.random.uniform(0,1), gamma) 
    print("Creating powerlaw edgelist")
    edge_list = generate_edges(degree_list)
    print("Plotting node coordinates")
    positions = generate_positions(edge_list)
    print("Creating Network Object")
    g = StaticNetwork()
    print("Creating Node Objects")
    for id, pos in positions.items():
        g.addNode(id,pos)
    print("Creating Edge Objects")
    for e in edge_list:
        g.addEdge(e)
    print("Done.")
    return g
"""

"""
def generate_positions(edge_list):
        g = nx.Graph(list(edge_list))
        print('geometric scale: ', len(g.nodes))
        positions = nx.spring_layout(g,scale=len(g.nodes), iterations=30)
        return positions
"""

"""
Strategy:
Take the static edge list and duplicate it. 
Randomly choose and remove edges from each duplicate 
Randomly choose two edges and do crossover on them.

Similar evolution rules from a genetic algorithm.
"""

"""
def evolve(g,mutation=0.1):
    dg = copy.deepcopy(g)
    removeEdges(dg,mutation)
    return dg

def removeEdges(g, percent=0.1):
    count = int(len(g.edges) * percent)
    print(g.edges.keys())
    removeList = random.choices(list(g.edges.keys()),k=count)
    print(removeList)
    for e in removeList:
        if g.edges.get(e):
            del g.edges[e]
            print('removing', e)

def swapEdges(g):
    return g

def buildPowerlawDataset(nodes=100, duration=30, mutation=0.1):
    masterNetwork = generate_powerlaw(nodes)
    dirName = f"powerlaw-{nodes}nodes-{duration}frames-removal-{mutation}"
    os.mkdir(dirName)
    for time in range(0, duration):
        #st.clock()
        path = os.path.join(dirName, f"{time:02d}.json")
        json = open(path,'w')
        #print("Creating string with "+str(len(st.stgNodes))+" nodes and "+str(len(st.stgEdges))+" edges.")
        st = evolve(masterNetwork, mutation)
        string = str(st)
        print("Writing file")
        json.write(string)
        json.flush()
        json.close()
        print("File written")
"""
