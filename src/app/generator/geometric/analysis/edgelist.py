"""
import datetime
from collections import defaultdict
data = [datetime.datetime(2019, 10, 20, 16, 37), datetime.datetime(2019, 10, 20, 16, 50, 7), datetime.datetime(2019, 11, 21, 16, 51, 47), datetime.datetime(2019, 11, 21, 10, 51, 20), datetime.datetime(2019, 10, 21, 10, 53, 22), datetime.datetime(2019, 11, 21, 10, 58, 27)]
snapshots = defaultdict(list)
ftime = "%Y-%m-%d-%H-%M-%S"
for i in data:
    key = i.strftime(ftime)
    snapshots[key].append(i)
"""

filename = 'sx-mathoverflow-a2q.txt'

def loadEdgeFile(filename):
    te = Temporal_Edgelist()
    """reads a graph file and loads into memory"""
    print(f'Loading {filename}')
    filedata = open(filename, 'r')
    edgelist = filedata.read().splitlines()
    for row in edgelist:
        #src, dst, time = map(int,row.split())
        node1, node2, time = map(int,row.split())               #ADDED for easy check of edges
        src, dst = min([node1,node2]), max([node1,node2])       #ADDED for easy check of edges
        te.addEdge([src,dst],time)      
    return te


from collections import defaultdict
import datetime
class Temporal_Edgelist:
    def __init__(self):
        self.nodes = set()
        self.edges = dict()
    def addEdge(self, edge, time):
        src, dst = min(edge), max(edge)
        if isinstance(time,int):
            time = datetime.datetime.fromtimestamp(time)
        e = Edge(src,dst,time=time)
        self.nodes |= {src, dst}
        self.edges[e.id] = e
    def discretize(self, ftime="%Y-%m-%d-%H-%M-%S"):
        snapshots = defaultdict(list)
        snapshots['nodes'] = self.nodes
        for id, edge in self.edges.items():
            key = edge.time.strftime(ftime)
            snapshots[key].append(edge.id)
        return snapshots
    def discretizeByYear(self):
        return self.discretize(ftime="%Y")
    def discretizeByMonth(self):
        return self.discretize(ftime="%Y-%m")
    def discretizeByDay(self):
        return self.discretize(ftime="%Y-%m-%d")
    def discretizeByHour(self):
        return self.discretize(ftime="%Y-%m-%d-%H")
    def discretizeByMinute(self):
        return self.discretize(ftime="%Y-%m-%d-%H-%M")
    def discretizeBySecond(self):
        return self.discretize()
    def calculate_positions(self):
        g = nx.Graph( [ re.findall("\d+", edge) for edge in self.edges.keys() ])
        print('geometric scale: ', len(g.nodes))
        self.nodes = nx.spring_layout(g,scale=len(g.nodes), iterations=10)
        #for id, pos in positions.items():
        #    g.addNode(id,pos)
                

class Edge:
    def __init__(self, src, dst, weight=1,time=None):
        self.id = f'({src},{dst})'
        self.src = src
        self.dst = dst 
        self.weight = weight
        self.time = time
    def __eq__(self, value):
        return isinstance(value, Edge) and value.id == self.id
    def __str__(self):
        return f'{{"source": "{self.src}", "target": "{self.dst}", "value": {self.weight}}}'



class Node:
    def __init__(self, id, pos=[None,None], group=1):
        self.id = id
        self.x, self.y = pos
        self.group = group
    def __eq__(self, value):
        return isinstance(value, Node) and value.id == self.id
    def __str__(self):
        """return f'{{"id": "{self.id}", "fx": {self.x}, "fy": {self.y}, "group": {self.group}}}' """
        coords = f'"fx": {self.x}, "fy": {self.y},' if (self.x != None and self.y != None) else ""
        return f'{{"id": "{self.id}", {coords} "group": {self.group}}}'
    def setCoordinate(self, position):
        self.x, self.y = position

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



class TemporalNetwork:
    def __init__(self):
        self.snapshots = []
    def get(self, index=0):
        return self.snapshots[index]
    def add(self, graph):
        self.snapshots.append(graph)
    def __len__(self):
        return len(self.snapshots)

import re
def tedgelist_to_tnet(te):
    tn = TemporalNetwork()
    #counter = 0
    for time in te.keys() - {'nodes'}:
        #counter += 1
        #print('time', counter, 'of', len(te.keys())-1 )
        network = StaticNetwork()
        #for node in te['nodes']:   
        #    network.addNode(node)
        for id,pos in te['nodes'].items():      #TED added for coords   
            network.addNode(id,pos)             #TED added for coords
        for edge in te[time]:
            src, dst = map(int, re.findall("\d+", edge))  
            network.addEdge([src,dst])
        tn.add(network)
    return tn

import os
def writeTN(tn, dirname='temp'):
    os.mkdir(dirname)
    for time in range(len(tn)):
        path = os.path.join(dirname, f"{time:02d}.json")
        json = open(path,'w')
        text = str(tn.get(time))
        print("Writing file")
        json.write(text)
        json.flush()
        json.close()
        print("File written")

def main():
    te = loadEdgeFile(filename)
    te.calculate_positions()
    teMonth = te.discretize("%Y-%m-%d-%H-%M")
    tn = tedgelist_to_tnet(teMonth)
    writeTN(tn, dirname='minutes')


import networkx as nx
def generate_positions(edge_list):
        g = nx.Graph(list(edge_list))
        print('geometric scale: ', len(g.nodes))
        positions = nx.spring_layout(g,scale=len(g.nodes), iterations=30)
        return positions


###########################################################

filename = 'sx-mathoverflow-a2q.txt'

def load_edgelist(filename):
    filedata = open(filename,'r')
    edgelist = filedata.read().splitlines()
    #arr = []
    for row in edgelist:
        node1, node2, time = map(int,row.split())
        #arr.append((node1, node2, time))
    #return arr



def loadEdgeFile(filename):
    te = Temporal_Edgelist()
    """reads a graph file and loads into memory"""
    print(f'Loading {filename}')
    filedata = open(filename, 'r')
    edgelist = filedata.read().splitlines()
    for row in edgelist:
        #src, dst, time = map(int,row.split())
        #te.addEdge([src,dst],time)
        node1, node2, time = map(int,row.split())
        src, dst = min([node1,node2]), max([node1,node2])
        te.addEdge([src,dst],time)
    return te
    

import datetime
class Temporal_Edgelist:
    def __init__(self):
        self.nodes = set()
        self.edges = dict()
    def addEdge(self, edge, time):
        src, dst = min(edge), max(edge)
        e = Edge(src,dst,time)
        self.nodes |= {src, dst}
        self.edges[e.id] = datetime.datetime.fromtimestamp(time)
    def get(self, duration):
        return None
        




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






