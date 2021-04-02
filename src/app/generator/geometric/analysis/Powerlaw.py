
import numpy as np
import random
import networkx as nx
import os
import copy

class Node:
    def __init__(self, id, pos=[None,None], group=1):
        self.id = id
        self.x, self.y = pos
        self.group = group
    def __eq__(self, value):
        return isinstance(value, Node) and value.id == self.id
    def __str__(self):
        return f'{{"id": "{self.id}", "fx": {self.x}, "fy": {self.y}, "group": {self.group}}}'
    def setCoordinate(self, position):
        self.x, self.y = position

class Edge:
    def __init__(self, src, dst, weight=1):
        self.id = f'({src},{dst})'
        self.src = src
        self.dst = dst 
        self.weight = weight
    def __eq__(self, value):
        return isinstance(value, Edge) and value.id == self.id
    def __str__(self):
        return f'{{"source": "{self.src}", "target": "{self.dst}", "value": {self.weight}}}'

class StaticNetwork:
    def __init__(self):
        self.nodes = dict()
        self.edges = dict()
    def addEdge(self, edge, weight=1):
        src, dst = min(edge), max(edge)
        e = Edge(src,dst,weight)
        self.edges[e.id] = e 
    def addNode(self, id, pos=[None, None], group=1):
        self.nodes[id] = Node(id,pos,group)
    def __str__(self):
        return f'{{"nodes": [{",".join( map(str,self.nodes.values()))}], "links": [{",".join(map(str,self.edges.values()))}]}}'


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

def draw_graph(edge_list):
    import matplotlib.pyplot as plt
    g = nx.Graph(list(edge_list))
    nx.draw(g)
    plt.show()

def power_law(k_min, k_max, y, gamma):
    return ((k_max**(-gamma+1) - k_min**(-gamma+1))*y  + k_min**(-gamma+1.0))**(1.0/(-gamma + 1.0))

def generate_powerlaw(nodes=100, k_min=1.0, k_max=100, gamma = 3.0):
    print("Generating Powerlaw Distribution")
    powerlaw_distribution = np.zeros(nodes, int)
    for n in range(nodes):
        powerlaw_distribution[n] = power_law(k_min, k_max, np.random.uniform(0,1), gamma) 
    print("Creating powerlaw edgelist")
    edge_list = powerlaw_edgelist(powerlaw_distribution)
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



def generate_positions(edge_list):
        g = nx.Graph(list(edge_list))
        print('geometric scale: ', len(g.nodes))
        positions = nx.spring_layout(g,scale=len(g.nodes), iterations=30)
        return positions


"""
Strategy:
Take the static edge list and duplicate it. 
Randomly choose and remove edges from each duplicate 
Randomly choose two edges and do crossover on them.

Similar evolution rules from a genetic algorithm.
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
