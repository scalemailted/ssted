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


import json
def readJSON(filename):
    """reads a graph file and loads into memory"""
    print(f'Loading {filename}')
    filedata = open(filename, 'r')
    network_data = json.load(filedata)
    network_data['nodes']
    network_data['links']
    graph = StaticNetwork()
    for node in network_data['nodes']:
        id,fx,fy,group = node.values()
        graph.addNode(id,[fx,fy],group)
    for edge in network_data['links']:
        src, dst, weight = edge.values()
        graph.addEdge([src,dst],weight)
    return graph

##########################################################

class TemporalNetwork:
    def __init__(self):
        self.snapshots = []
    def get(self, index=0):
        return self.snapshots[index]
    def add(self, graph):
        self.snapshots.append(graph)
    def __len__(self):
        return len(self.snapshots)

def readTN(filenames):
    tn = TemporalNetwork()
    for name in filenames:
        network = readJSON(name)
        tn.add(network)
    return tn

def getFilenames(dirname,start=0, end=29):
    filenames = []
    for name in range(start,end+1):
        path = f'{dirname}/{name:02d}.json'
        filenames.append(path)
    return filenames


#########################################################

def walk(tnet, srcId, start=0, end=1 ):
    #print('Starting network walk... Start: ', srcId)
    delta, path = {srcId: 0.0}, {srcId: [srcId]}
    #print('start weights: ',delta, 'start path:', path)
    for time in range(start,end):
        #print("Time: ", time)
        _, edges = tnet.get(time, time+1)
        for e in edges:
            #print('Checking edge: ', e)
            #print('Check Source Node: ', e.src, ' in keys:', delta.keys())
            if e.src in delta:
                #if (delta.get(e.dst) or float('inf'))  > delta[e.src] + e.weight:
                if (float('inf') if delta.get(e.dst) is None else delta.get(e.dst)) > delta[e.src] + e.weight:
                    #print('Update [Old Weights]:', delta)
                    delta[e.dst] = delta[e.src] + e.weight
                    path[e.dst] = path[e.src] + [e.dst]
                    #print('Update:', e.dst, 'Weight:',delta[e.dst])
            #since duplicate edges don't exist in model
            elif e.dst in delta:
                #print('Evaluate weights')
                #if (delta.get(e.src) or float('inf'))  > delta[e.dst] + e.weight:
                if (float('inf') if delta.get(e.src) is None else delta.get(e.src)) > delta[e.dst] + e.weight:
                    #print('Update [Old Weights]:', delta)
                    delta[e.src] = delta[e.dst] + e.weight
                    path[e.src] = path[e.dst] + [e.src]
                    #print('Update:', e.src, 'New Weight:',delta[e.src])
    return (delta, path)


def get_shortest_paths(tnet, start=0, end=1):
    nodes, _ = tnet.get(start,end)
    path_data = {}
    for n in nodes:
        print('walking',n)
        delta, path = walk(tnet, n, start, end )
        path_data[n] = {'paths':path, 'delta': delta}
    return path_data     


##################################################################

#filenames = getFilenames('powerlaw-10nodes-30frames',0,29)
#tn = readTN(filenames)


### Centrality Measures ###

#nodal measure
#returns node degree for each snapshot, how active the node is for each time frame
def temporal_degree_centrality(tnet):
    print("calculating... temporal degree centrality")
    times = len(tnet)
    nodes = tnet.nodes
    degrees =   {n: [0] * times for n in nodes}#[node][time]
    for t in range(times):
        _, edges = tnet.get(t,t+1)
        #edges = network.edges.values()
        for e in edges:
            degrees[e.src.id][t] += 1
            degrees[e.dst.id][t] += 1
    return degrees

#network measure
#returns total sum of all node degree for every snapshot, how active the node is for all times
def temporal_degree_centrality_overall(degrees):
    degree_totals = {}
    for node in degrees:
        degree_totals[node] = sum(degrees[node])
    return degree_totals


import math
#network measure
def topological_overlap_overall(tnet):
    print("Calculating... topological overlap")
    times = len(tnet)
    #nodes = tnet.get(0).nodes
    #overlaps = {n:[None] * times for n in nodes}
    overlaps = []
    for t in range(times-1):
        #tn_now = tnet.get(t)
        #tn_next = tnet.get(t+1)
        _, edges_now = tnet.get(t,t+1)
        _, edges_next = tnet.get(t+1,t+2)
        #edges_now = set(edges_now.keys())
        #edges_next = set(edges_next.keys())
        #print("edges now: ", edges_now)
        #print("edges next: ", edges_next)
        #print(edges_now & edges_next)
        #print(len(edges_now & edges_next) / math.sqrt(len(edges_now | edges_next)))
        #jaccard = len(edges_now & edges_next) / math.sqrt(len(edges_now | edges_next))
        jaccard = len(edges_now & edges_next) / (len(edges_now | edges_next))
        #2021-3-5
        now_set = set([e.id for e in edges_now])
        next_set = set([e.id for e in edges_next])
        jaccard = len(now_set & next_set) / (len( now_set | next_set))
        overlaps.append(jaccard)
    return overlaps

'''
#nodal measure
def topological_overlap(tnet):
    print("Calculating... topological overlap")
    times = len(tnet)
    nodes = tnet.get(0).nodes
    overlaps = {n:[0] * times for n in nodes}
    for t in range(times-1):
        tn_now = tnet.get(t)
        tn_next = tnet.get(t+1)
        edges_now = set(tn_now.edges.keys())
        edges_next = set(tn_next.edges.keys())
        #jaccard = len(edges_now & edges_next) / math.sqrt(len(edges_now | edges_next))
        intersect = edges_now & edges_next
        union = edges_now | edges_next
        for eid in intersect:
            print('eid', eid)
            edge = tn_now.edges[eid]
            print('edge', edge)
            overlaps[edge.src][t] += 1
            overlaps[edge.dst][t] += 1            
    return overlaps
'''



#nodal measure
def topological_overlap(tnet):
    print("Calculating... topological overlap")
    times = len(tnet)
    nodes = tnet.nodes
    overlaps = {n:[0] * (times-1) for n in nodes}
    for t in range(times-1):
        _, edges_now = tnet.get(t,t+1)
        _, edges_next = tnet.get(t+1,t+2)
        #edges_now = set(tn_now.edges.keys())
        #edges_next = set(tn_next.edges.keys())
        #jaccard = len(edges_now & edges_next) / math.sqrt(len(edges_now | edges_next))
        intersect = edges_now & edges_next
        differnece = edges_now ^ edges_next

        #TODO START hacked 2021-3-5
        now_set = set([e.id for e in edges_now])
        next_set = set([e.id for e in edges_next])
        intersect_set = now_set & next_set
        differnece_set = now_set ^ next_set
        intersect = set([ tnet.edges[e] for e in intersect_set ])
        differnece = set([ tnet.edges[e] for e in differnece_set ])
        #TODO END hacked 2021-3-5

        numerators = {n:0  for n in nodes}
        denominators = {n:0 for n in nodes}
        for eid in intersect:
            edge = eid #tnet.edges[eid.id]
            numerators[edge.src.id] += 1
            numerators[edge.dst.id] += 1
            denominators[edge.src.id] += 1
            denominators[edge.dst.id] += 1
        for eid in differnece:
            #edge = edges_now.get(eid) or edges_next.get(eid)
            edge = eid
            denominators[edge.src.id] += 1
            denominators[edge.dst.id] += 1
        for n in nodes:
            #overlaps[n][t] = numerators[n] / ( math.sqrt(denominators[n]) or 1)   
            overlaps[n][t] = numerators[n] / ( denominators[n] or 1)  
    return overlaps

import numpy as np
#nodal measure, use previous method
def topological_overlap_average(overlaps):
    overlap_averages = {}
    for n in overlaps:
        overlap_averages[n] = np.mean(overlaps[n])
    return overlap_averages

#network measure, use previous method
def temporal_correlation_coefficient(nodal_averages):
    return np.mean(list( nodal_averages.values() ))


###########################################################
'''
#Intercontact times
def intercontact_times(tnet):
    print("computing... intercontact times")
    icts = {}
    for t in range(len(tnet)):
        g = tnet.get(t)
        edges = g.edges.keys()
        for e in edges:
            if not icts.get(e):
                #icts[e] = [t]
                icts[e] = [(t,t or 1)]
            else:
                #icts.append(t)
                prev_t, _ = icts[e][-1]
                icts[e] += [(t, t-prev_t)]
    return icts
'''

def intercontact_times(tnet):
    print("computing... intercontact times")
    icts = {}
    prev_t = {}
    for t in range(len(tnet)):
        g, edges = tnet.get(t,t+1)
        #edges = g.edges.keys()
        for e in edges:
            if not icts.get(e.id):
                #icts[e] = [t]
                icts[e.id] = [t or 1]
                prev_t[e.id] = t
            else:
                #icts.append(t)
                icts[e.id].append( t - prev_t[e.id] )
                prev_t[e.id] = t
    return icts


#requires previous method
#When B > 0, indicates bursty intercontact times. When B < 0, indicates periodic/tonic intercontact times. When B = 0, indicates random.
def bursty_coeff(icts):
    edge_coeff = {}
    for i in icts:
        edge_coeff[i] = (np.std(icts[i]) - np.mean(icts[i])) / (np.std(icts[i]) + np.mean(icts[i]))
    return edge_coeff

#requires previous method
#The possible range is: 0≥𝐿𝑉>3.
#When periodic, LV=0, Poisson, LV=1 Larger LVs indicate bursty process.
def local_variation(icts):
    print("computing... local variations")
    lvs = {}
    for e in icts:
        summa = 0
        n = len(icts[e])
        for i in range(n-1):
            event_now = icts[e][i]
            event_next = icts[e][i+1]
            summa += (event_now - event_next)**2 / (event_now + event_next)
        lvs[e] = 3/((n-1) or 1) * summa
    return lvs

#################################################################

# Temporal Betweenness Centrality
def betweenness_centrality(path_data):
    n = len(path_data)
    betweenness = {}
    for node in path_data:
        counter = count_node_in_paths(path_data, node)
        #betweenness[node.id] = 1/((n-1)*(n-2)) * counter
        betweenness[node.id] = 1/(n-1) * counter
        #betweenness[node.id] =  counter
    return betweenness

#(helper for betweenness)
#Counts the appearance of node in all other paths 
def count_node_in_paths(paths, node_to_check):
    counter = 0;
    for node in paths: 
        if node != node_to_check:
            counter += list(paths[node]['paths']).count(node_to_check)
    return counter


# Temporal Closeness Centrality
def closeness_centrality(path_data):
    n = len(path_data)
    closeness = {}
    for node in path_data:
        #path_deltas = path_data[node]['delta'].values()
        #closeness[node.id] = 1/(n-1) * sum(path_deltas)
        counter = count_node_hops(path_data, node)
        closeness[node.id] = 1/(n-1) * counter
    return closeness

#(helper for closeness)
#Counts the inverse count in hops, (1/hops),
#thus larger hops is smaller number
#no hops is 0
def count_node_hops(paths, node_to_check):
    counter = 0
    for node in paths:
        hops = paths[node]['delta'].get(node_to_check)
        counter +=  1/hops if hops else 0
    return counter

        
