#powerlaw distribution defines bursty broadcast (node degrees) in network

import numpy as np
import random
import os

## Add parameter burstiness via percentage of nodes
## generate burstiness measures between old graph and new graph 

class BurstyNetwork:
    def __init__(self):
        self.nodes = set()
        self.edges = set()
        self.start_time = None
        self.end_time = None
        self.dt = None

def powerlaw(k_min, k_max, y, gamma):
    return ((k_max**(-gamma+1) - k_min**(-gamma+1))*y  + k_min**(-gamma+1.0))**(1.0/(-gamma + 1.0))

def generate_nodal_edge_event_counts(timeframes=10, nodes=100,k_min=1.0, k_max=100, gamma = 3.0):
    print("Generating a node's temporal degree")
    temporal_degrees_for_node = np.zeros(timeframes, int)
    for t in range(timeframes):
        temporal_degrees_for_node[t] = powerlaw(k_min, k_max, np.random.uniform(0,1), gamma) 
    return temporal_degrees_for_node

def generate_bursty_network_nodes(size=20,frames=10):
    node_events = {}
    for i in range(size):
        temporal_degrees = generate_nodal_edge_event_counts(frames,size,k_min=1.0, k_max=20, gamma = 3.0)
        node_events[i] = temporal_degrees
    return node_events

"""
def generate_bursty_network_edges(node_events, prior_edges=None):
    frames = len(node_events[0])
    edges = {}
    for t in range(frames):
        edges[t] = set()
        remaining_degrees = [n for n in node_events for i in range(node_events[n][t])]
        for node in sorted(node_events,key=lambda x:sum(n[x])):  #node_events:
            try :
                remaining_degrees.remove(node)
            except:
                print(str(node) + " not in remanining degrees")
            print("node: [" + str(node) + "] @ time:["+str(t)+"]"+" degree: [" + str(node_events[node][t])+"]")
            possible_links = {n for n in remaining_degrees if n != node}
            degree = node_events[node][t]
            links = random.sample(possible_links, min([degree,len(possible_links)]))
            for e in links:
                remaining_degrees.remove(e)
                edges[t] |= {(node,e)}
    return edges
"""

def generate_bursty_network_edges(node_events):
    frames = len(node_events[0])
    edges = {}
    priors = {}
    for t in range(frames):
        edges[t] = set()
        remaining_degrees = [n for n in node_events for i in range(node_events[n][t])]
        #for node in sorted(node_events,key=lambda x:sum(node_events[x]),reverse=True):  #node_events:
        #for node in node_events:  #node_events:
        for node in sorted(node_events,key=lambda x:sum(node_events[x])):
            if node in remaining_degrees:
                remaining_degrees.remove(node)
            print("node: [" + str(node) + "] @ time:["+str(t)+"]"+" degree: [" + str(node_events[node][t])+"]")
            possible_links = {n for n in remaining_degrees if n != node}
            degree = node_events[node][t]
            links = []
            if node in priors:
                #link = random.sample(edges[t-1], min([degree,len(edges[t-1])]))
                links = random.sample(priors[node], min([degree,len(priors[node])]))
                print("Time:"  + str(t) + " Degree: " + str(degree) + " Priors: " + str(len(links)))
                if len(links) < degree:
                    print("Need more edges: " + str(degree-len(links)))
                    link = random.sample(possible_links, min([degree-len(links),len(possible_links)]))
                    links.append(link)
            else:
                priors[node] = set()
                links = random.sample(possible_links, min([degree,len(possible_links)]))
            print("links: ", links)
            for e in links:
                if e in remaining_degrees:
                    remaining_degrees.remove(e)
                    edges[t] |= {(node,e)}
                    priors[node].add(e)
    return edges

def generateTGraphs():
    node_events = generate_bursty_network_nodes()
    edges = generate_bursty_network_edges(node_events)
    positions = generate_positions(edges[0])
    graphs = []
    for t in range(len(node_events[0])):
        print("for-loop")
        g = StaticNetwork()
        for id, pos in positions.items():
            g.addNode(id,pos)
        print("nodes complete")
        for e in edges[t]:
            g.addEdge(e)
        print("edges complete")
        graphs.append(g)
    return graphs

def printJSON():
    graphs = generateTGraphs()
    nodes = 20
    duration = 10
    dirName = f"burstiness-{nodes}nodes-{duration}frames"
    os.mkdir(dirName)
    for time in range(0, duration):
        path = os.path.join(dirName, f"{time:02d}.json")
        json = open(path,'w')
        st = graphs[time]
        string = str(st)
        print("Writing file")
        json.write(string)
        json.flush()
        json.close()
        print("File written")


#print("Creating powerlaw edgelist")
#edge_list = powerlaw_edgelist(powerlaw_distribution)
#print("Plotting node coordinates")
#positions = generate_positions(edge_list)
#print("Creating Network Object")
#g = StaticNetwork()
#print("Creating Node Objects")
#for id, pos in positions.items():
#    g.addNode(id,pos)
#print("Creating Edge Objects")
#for e in edge_list:
#    g.addEdge(e)
#print("Done.")
#return g

def draw_graph(edge_list):
    import networkx as nx
    import matplotlib.pyplot as plt
    g = nx.Graph(list(edge_list))
    nx.draw(g)
    plt.show()

def generate_positions(edge_list):
        import networkx as nx
        g = nx.Graph(list(edge_list))
        print('geometric scale: ', len(g.nodes))
        positions = nx.spring_layout(g,scale=len(g.nodes), k=5,iterations=30)
        return positions



class Node:
    def __init__(self, id, pos=[None,None], group=1):
        self.id = id
        self.x, self.y = pos
        self.group = group
    def __eq__(self, value):
        return isinstance(value, Node) and value.id == self.id
    def __str__(self):
        return f'{{"id": "{self.id}", "group": {self.group}}}'
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
