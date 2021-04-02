from ..models.network import *

import numpy as np
import random
import networkx as nx

def generate_degrees(function, nodes=100, *args):
    degree_list = np.zeros(nodes, int)
    for n in range(nodes):
        degree_list[n] = function( *args) 
    return tuple(degree_list)

def generate_edges(node_degrees):
    edge_list = set()
    node_ids = tuple(range(len(node_degrees)))
    for id, degree in zip(node_ids, node_degrees):
        other_nodes = node_ids[:id] + node_ids[id+1:]
        other_degrees = node_degrees[:id] + node_degrees[id+1:]
        neighbors = random.choices(other_nodes,weights=other_degrees,k=degree)
        edge_list |= {tuple(sorted([id, n])) for n in neighbors}
    return edge_list

def generate_positions(edge_list):
        g = nx.Graph(list(edge_list))
        positions = nx.spring_layout(g,scale=len(g.nodes), iterations=10)
        return positions

#def generate_tnet(edge_list):
def generate_tnet(edge_list,  isForced=False):
    tnet = TemporalNetwork()
    #print(map(str,tnet.nodes.values()))
    for e in edge_list:
        src, dst = e
        te = TemporalEdge(src,dst)
        tnet.add_edge(te)
    #print(map(str,tnet.nodes.values()))
    if isForced:                    #added as hack
        return tnet                 #added as hack
    positions = generate_positions(edge_list)
    for id, pos in positions.items():
        x,y = pos
        coord = Position(x,y)
        tnet.nodes[id].set_position(coord)
    return tnet


#generates all network snapshots via random (guassian) function
def evolve(tnet, steps, probability):
    for e in tnet.edges.values():
        #if probability >= random.random():
        count = random.randint(1,steps/2) + random.randint(1,steps/2) #randomizer function
        occurences = frozenset( random.sample(list(range(steps)),k=count) )
        tnet.add_edge(e,occurences) 

#[tester] generates all network snapshots via bursty (powerlaw) function
#def evolve_bursty(tnet, steps):




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