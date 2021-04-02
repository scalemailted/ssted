"""
#old implementation using sets
class TemporalNetwork:
    def __init__(self):
        self.nodes = set()
        self.edges = set()
        self.timestamps = set()
    def get_frame(self, index=0):
        return self.snapshots[index]
    def add_node(self, node):
        self.nodes.add(node)
    def add_nodes(self, nodes):
        self.nodes |= set(nodes)
    def add_edge(self, edge):
        self.timestamps.add(edge.occurences)
        self.nodes |= set([edge.src, edge.dst])
        if edge in self.edges:
            self.edges[edge] += edge
        else:
            self.edges.add(edge)
    def __len__(self):
        return len(self.timestamps)
    def __str__(self):
        return f'{{"snapshots":  {len(self.timestamps)}, "nodes": {len(self.nodes)}, "edges:" {len(self.edges)}}}'
"""

"""
class TemporalNetwork:
    def __init__(self):
        self.nodes = dict()
        self.edges = dict()
        self.timestamps = set()
        
    def next(self, start=0, end=1, step=1):
        return ""
    
    def add_node(self, node=None, pos=None, group=1):
        if isinstance(node, Node):
            self.nodes[node.id] = node
        elif node:
            self.nodes[node] = Node(node, pos, group)
    
    def add_nodes(self, nodes):
        if isinstance(nodes, dict):
            self.nodes |= nodes
        elif isinstance(nodes, (list, set, frozenset, tuple)):
            self.nodes |= {n.id: n for n in nodes}
    
    def add_edge(self, edge):
        self.add_nodes( [edge.src, edge.dst] )
        self.timestamps |=  edge.occurences
        if edge in self.edges:
            self.edges[edge.id] += edge
        else:
            self.edges[edge.id] = edge
    
    def __len__(self):
        return len(self.timestamps)
        
    def __str__(self):
        return f'{{"snapshots":  {len(self.timestamps)}, "nodes": {len(self.nodes)}, "edges:" {len(self.edges)}}}'
"""
from collections import defaultdict
class TemporalNetwork:
    def __init__(self):
        self.nodes = dict()
        self.edges = dict()
        self.timestamps = defaultdict(set) 
        #self.timestamps = dict()
        #self.timestamps = set()
        
    def get(self, start=0, end=1):
        edgelist = { edge for (time,edges) in self.timestamps.items() for edge in edges if start <= time < end }
        #edgelist = set()
        #for time,edges in self.timestamps.items():
        #    if start <= time <= end:
        #        edgelist |= edges
        #    if time >= end:
        #        break
        return (self.nodes.values(), edgelist)
    
    def add_node(self, node=None, pos=None, group=1):
        if isinstance(node, Node):
            self.nodes[node.id] = node
        elif node:
            self.nodes[node] = Node(node, pos, group)

    def add_tnode(self, node=None, pos=None, time=None, group=1):
        if isinstance(node, TemporalNode):
            if not self.nodes.get(node.id):
                self.nodes[node.id] = node
            self.nodes[node.id].set_position(time,pos) 
        elif node:
            print('node',node)
            if not self.nodes.get(node):
                self.nodes[node] = TemporalNode(node, group)
            self.nodes[node].set_position(time,pos) 
    
    def add_nodes(self, nodes):
        if isinstance(nodes, dict):
            print("untested")
            self.nodes.update(nodes)
        elif isinstance(nodes, (list, set, frozenset, tuple)):
            self.nodes.update({n.id: n for n in nodes if not n.id in nodes})
    
    def add_edge(self, edge, *times):
        self.add_nodes( [edge.src, edge.dst] )
        if times:
            edge.occurences |= set(*times)
        #self.timestamps |= { time: edge for time in edge.occurences} 
        for time in edge.occurences:
            self.timestamps[time].add(edge)
        if edge in self.edges:
            self.edges[edge.id] += edge
        else:
            self.edges[edge.id] = edge
    
    #refactor this with above method
    def add_edge_without_nodes(self, edge, *times):
        if times:
            edge.occurences |= set(*times)
        #self.timestamps |= { time: edge for time in edge.occurences} 
        for time in edge.occurences:
            self.timestamps[time].add(edge)
        if edge in self.edges:
            self.edges[edge.id] += edge
        else:
            self.edges[edge.id] = edge
    
    def get_neighbor_edges(self, node):
        #return [ edge.id for edge in self.edges.values() if node in (edge.src.id, edge.dst.id) ]
        return { edge.id for edge in self.edges.values() if edge.contains(node) }
    
    def __len__(self):
        return len(self.timestamps)
        
    def __str__(self):
        return f'{{"snapshots":  {len(self.timestamps)}, "nodes": {len(self.nodes)}, "edges:" {len(self.edges)}}}'
        
    
    

class TemporalEdge:
    def __init__(self, src, dst, *times):
        if isinstance(src, Node):
            self.src = src
        else:
            self.src = Node(src)
        if isinstance(dst, Node):
            self.dst = dst
        else:
            self.dst = Node(dst)
        self.occurences = frozenset(times)
        self.weight = 1
        self.id = f'({self.src.id},{self.dst.id})'
    
    def add(self, other):
        if isinstance(other, TemporalEdge) and self == other:
            self.occurences |= other.occurences
        elif isinstance(other, (int, float, complex)):
            self.occurences.add(other)
        elif isinstance(other, (tuple,list,set,frozenset)): #ADDED [NO TEST]
            self.occurences |= set(other) 
    
    def contains(self, node):
        if isinstance(node, (str,int)):
            return node in (self.src.id, self.dst.id)
        else:
            return node in (self.src, self.dst)
            
    def __add__(self, other):
        if isinstance(other, TemporalEdge) and self == other:
            times = self.occurences | other.occurences 
            return TemporalEdge(self.src, self.dst, *times)
        elif isinstance(other, (int, float, complex)):
            times = self.occurences | set([other]) 
            return TemporalEdge(self.src, self.dst, *times)
        elif isinstance(other, (tuple,list,set,frozenset)): #ADDED [NO TEST]
            times = self.occurences | set(other) 
            return TemporalEdge(self.src, self.dst, *times)
    
    def __eq__(self, other):
        return isinstance(other, TemporalEdge) and self.src == other.src and self.dst == other.dst
    
    def __len__(self):
        return len(self.occurences)
    
    def __str__(self):
        return f'{{"source": "{self.src.id}", "target": "{self.dst.id}", "value": {self.weight}}}'
    
    def __hash__(self):
        return id(self)


class Node:
    def __init__(self, id, pos=None, group=1):
        self.id = id 
        self.pos = pos
        self.group = group
    
    def __hash__(self):
        return int(self.id)
    
    def __eq__(self, value):
        return isinstance(value, Node) and value.id == self.id
    
    def __str__(self):
        pos_str = f' "fx": {self.pos.x}, "fy": {self.pos.y},' if self.pos else ""
        return f'{{"id": "{self.id}",{pos_str} "group": {self.group}}}'
    
    def set_position(self, position):
        self.pos = position

class Position:
    def __init__(self, x, y, z=None):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        z_str = "" if self.z == None else f', "z": {self.z}'
        return f'{{"x": {self.x}, "y": {self.y}{z_str}}}'


class StaticNetwork:
    def __init__(self, nodes=None, edges=None):
        self.nodes = set()
        self.edges = set()
        for n in nodes:
            self.add_node(n)
        for e in edges:
            self.add_edge(e)
    
    def add_edge(self, edge):
        #self.add_node(edge.src)
        #self.add_node(edge.dst)
        self.edges.add(edge)
    
    def add_node(self, node):
        self.nodes.add(node)
    
    def __str__(self):
        nodes =  ",".join( map(str,self.nodes))
        links =  ",".join( map(str,self.edges))
        return f'{{"nodes": [{nodes}], "links": [{links}]}}'


#TODO Model Temporal Nodes --> move position over time
#Needed for Geometric Network
class TemporalNode:
    def __init__(self, id, group=1):
        self.id = id 
        self.positions = dict()
        self.group = group
    
    def __hash__(self):
        return int(self.id)
    
    def __eq__(self, value):
        return isinstance(value, Node) and value.id == self.id
    
    def __str__(self):
        #pos_str = f' "fx": {self.positions[0].x}, "fy": {self.positions[0].y},' if len(self.positions)==1 else ""
        pos_str = ""
        return f'{{"id": "{self.id}",{pos_str} "group": {self.group}}}'
    
    def set_position(self, time, position):
        self.positions[time] = position
    
    def at_time(self, time):
        return Node(self.id, self.positions[time])
        #pos_str = f' "fx": {self.positions[time].x}, "fy": {self.positions[time].y},' if self.positions.get(time) else ""
        #return f'{{"id": "{self.id}",{pos_str} "group": {self.group}}}'

import random

#schedules the occurrence for each node according its broadcast type and edge icts 
class Event_Scheduler:
    def __init__(self, tnet, steps=1, bias='node'):
        self.bias = bias
        self.steps = steps
        self.tnet = tnet
        self.events = { node: tnet.get_neighbor_edges(node) for node in tnet.nodes }
        self.node_bandwidths = { node:[0]*steps for node in tnet.nodes  }
        #self.events = defaultdict(set)
        #for node in tnet.nodes:
        #    self.events[node] = tnet.get_neighbor_edges(node)
    def execute(self, args):
        #emitters = {'gaussian':generate_gaussian_frames:,'uniform':generate_uniform_frames,'periodic':generate_periodic_frames,'bursty':generate_bursty_frames}
        #fxn = emitters[args.emitter_type]
        for node,edges in self.events.items():
            max_degree = len(edges)
            emitter_type = args['emitter_type']
            if emitter_type == 'gaussian':
                frame_degrees = generate_gaussian_frames(self.steps, max_degree ,float(args['events_min_rate']), int(args['events_duration']), float(args['events_activity_rate']))
            elif emitter_type == 'uniform':
                frame_degrees = generate_uniform_frames(self.steps, max_degree, float(args['events_min_rate']), int(args['events_duration']), float(args['events_activity_rate']))
            elif emitter_type == 'periodic':
                frame_degrees = generate_periodic_frames(self.steps, max_degree, float(args['events_min_rate']), int(args['events_duration']))
            elif emitter_type == 'bursty':
                frame_degrees = generate_bursty_frames(self.steps, max_degree, float(args['events_min_rate']), int(args['events_duration']))
            self.node_bandwidths[node] = frame_degrees
        for id,edge in self.tnet.edges.items():
            src = edge.src.id
            dst = edge.dst.id
            #bidir = self.node_bandwidths[src] and self.node_bandwidths[dst]
            for time in range(self.steps):
                if self.node_bandwidths[src][time] > 0 and self.node_bandwidths[dst][time] > 0:
                    #edge += time
                    #self.tnet.edges[id] += time
                    #self.tnet.add_edge(edge,[time])
                    self.tnet.add_edge_without_nodes(edge,[time])
                    self.node_bandwidths[src][time] -= 1
                    self.node_bandwidths[dst][time] -= 1
                elif self.node_bandwidths[src][time] > 0 or self.node_bandwidths[dst][time] > 0:
                    if random.randint(0,1) > 0:
                        #edge += time
                        #self.tnet.edges[id] += time
                        #self.tnet.add_edge(edge,[time])
                        self.tnet.add_edge_without_nodes(edge,[time])
                        self.node_bandwidths[src][time] -= 1
                        self.node_bandwidths[dst][time] -= 1
    def gaussian(self):
        for node,edges in self.events.items():
            max_degree = len(edges)
            for time in range(self.steps):
                local_degree = random.randint(0,max_degree//2) + random.randint(0,(max_degree+1)//2)
                self.node_bandwidths[node][time] = local_degree
        for id,edge in self.tnet.edges.items():
            src = edge.src.id
            dst = edge.dst.id
            #bidir = self.node_bandwidths[src] and self.node_bandwidths[dst]
            for time in range(self.steps):
                if self.node_bandwidths[src][time] > 0 and self.node_bandwidths[dst][time] > 0:
                    #edge += time
                    #self.tnet.edges[id] += time
                    self.tnet.add_edge(edge,[time])
                    self.node_bandwidths[src][time] -= 1
                    self.node_bandwidths[dst][time] -= 1
                elif self.node_bandwidths[src][time] > 0 or self.node_bandwidths[dst][time] > 0:
                    if random.randint(0,1) > 0:
                        #edge += time
                        #self.tnet.edges[id] += time
                        self.tnet.add_edge(edge,[time])
                        self.node_bandwidths[src][time] -= 1
                        self.node_bandwidths[dst][time] -= 1
    def static(self):
        for node,edges in self.events.items():
            max_degree = len(edges)
            for time in range(self.steps):
                local_degree = max_degree
                self.node_bandwidths[node][time] = local_degree
        for id,edge in self.tnet.edges.items():
            src = edge.src.id
            dst = edge.dst.id
            #bidir = self.node_bandwidths[src] and self.node_bandwidths[dst]
            for time in range(self.steps):
                if self.node_bandwidths[src][time] > 0 and self.node_bandwidths[dst][time] > 0:
                    #edge += time
                    #self.tnet.edges[id] += time
                    self.tnet.add_edge(edge,[time])
                    self.node_bandwidths[src][time] -= 1
                    self.node_bandwidths[dst][time] -= 1
                elif self.node_bandwidths[src][time] > 0 or self.node_bandwidths[dst][time] > 0:
                    if random.randint(0,1) > 0:
                        #edge += time
                        #self.tnet.edges[id] += time
                        self.tnet.add_edge(edge,[time])
                        self.node_bandwidths[src][time] -= 1
                        self.node_bandwidths[dst][time] -= 1
    def __len__(self):
        return len(self.events)
    def __str__(self):
        return f'[Event Scheduler] nodes: {len(self.events)}, links: {len(self.tnet.edges)}, events: {0}, bias: {self.bias}' 





##############################################################
# determine # of events based on duration & distribution & probability
# - Distribution

#Step0: create empty degrees list for each snapshot
#Step 1: determine ACTIVE VS INACTIVE STATES using emitter types: constant, uniform, gaussian, bursty, peridoic 
#Step 2: determine duration of event
#Step 3: determine minimal temproal degree --> 0, 25%, 50%, 75%, 100%
#Step 4: max degree occurence probability on active state
#Step 5: normalize results for mix of full versus partial degrees
#Step 6: compute bandwidth for each time step



#TED: DONE - [Note] refactor min degree as ratio from max degree
def generate_bursty_frames(frames,max_deg,min_deg=0,duration=1):
    #Step 0: create empty list for the node degree for each snapshot
    degree_per_frame = []
    while len(degree_per_frame) < frames:
        #Step 1: determine ACTIVE VS INACTIVE STATES using emitter types: bursty 
        degree = int(powerlaw_bursty(1,max_deg,gamma=3))
        #[X] Step 2: determine minimal temproal degree --> 0, 25%, 50%, 75%, 100%
        #[X] degree = int(probability * max_deg) if probability * max_deg > degree else degree
        #[X] degree = min_deg if degree and min_deg > degree else degree
        #Step 2: randomize between min/max degree 
        min_int = int(max_deg*min_deg)
        degree = random.randint(min_int, max_deg) if degree else 0
        #Step 3: max degree occurence probability on active state
        #degree = max_deg if degree and probability >= random.uniform(0,1) else degree
        #Step 4: determine duration of event
        for i in range(duration):
            if len(degree_per_frame) < frames:
                degree_per_frame.append(degree)
    return degree_per_frame

#TED: DONE - [Note] refactor min degree as ratio from max degree
def generate_periodic_frames(frames,max_deg,min_deg,duration=1):
    #Step 0: create empty degrees list for each snapshot
    degree_per_frame = []
    is_active = random.randint(0,1)
    while len(degree_per_frame) < frames:
        ##Step 1: determine ACTIVE VS INACTIVE STATES using emitter types: periodic
        degree = 0
        if is_active:
            #Step 2: randomize between min/max degree 
            #degree = random.randint(min_deg, max_deg)
            min_int = int(max_deg*min_deg)
            degree = random.randint(min_int, max_deg)
            #Step 3: max degree occurence probability on active state
            #degree = max_deg if degree and probability >= random.uniform(0,1) else degree
            #Step 4: determine duration of event
        for i in range(duration):
                if len(degree_per_frame) < frames:
                    degree_per_frame.append(degree)
        is_active = not is_active
    return degree_per_frame


#TED: DONE - [Note] refactor min degree as ratio from max degree
def generate_gaussian_frames(frames,max_deg,min_deg,duration=1,probability=0.5):
    #Step 0: create empty degrees list for each snapshot
    degree_per_frame = []
    while len(degree_per_frame) < frames:
        ##Step 1: determine ACTIVE VS INACTIVE STATES using emitter types: probability
        degree =  1 if random.uniform(0,1) < probability else 0
        if degree:
            #Step 2: randomize between min/max degree 
            min_int = int(max_deg*min_deg)
            degree = int((random.randint(min_int, max_deg) + random.randint(min_int, max_deg))/2)
        #Step 3: determine duration of event
        for i in range(duration):
                if len(degree_per_frame) < frames:
                    degree_per_frame.append(degree)
    return degree_per_frame


#TED: DONE - [Note] refactor min degree as ratio from max degree
def generate_uniform_frames(frames,max_deg,min_deg,duration=1,probability=0.5):
    #Step 0: create empty degrees list for each snapshot
    degree_per_frame = []
    while len(degree_per_frame) < frames:
        ##Step 1: determine ACTIVE VS INACTIVE STATES using emitter types: probability
        degree =  1 if random.uniform(0,1) < probability else 0
        if degree:
            #Step 2: randomize between min/max degree 
            min_int = int(max_deg*min_deg)
            degree = random.randint(min_int, max_deg)
        #Step 3: determine duration of event
        for i in range(duration):
                if len(degree_per_frame) < frames:
                    degree_per_frame.append(degree)
    return degree_per_frame


def powerlaw_bursty(k_min=1, k_max=1, gamma=3.0, y=None):
    y = y if y else np.random.uniform(0,1)
    return ((k_max**(-gamma+1) - k_min**(-gamma+1))*y  + k_min**(-gamma+1.0))**(1.0/(-gamma + 1.0))-1


'''
#Test
steps = 20
degrees = []
emit_duration = 3
max_degree = 6 
while len(degrees) < steps:
    deg = int(powerlaw_bursty(1,max_degree,gamma=3))
    for i in range(emit_duration):
        degrees.append(deg)
        if len(degrees) == steps:
            break
'''



#TODO import distribution functions and make them more geenric
import numpy as np
import random
'''
def powerlaw_bursty(k_min=1, k_max=1, gamma=3.0, y=None):
    y = y if y else np.random.uniform(0,1)
    return ((k_max**(-gamma+1) - k_min**(-gamma+1))*y  + k_min**(-gamma+1.0))**(1.0/(-gamma + 1.0))-1

def random_uniform(k_min=0, k_max=1):
    return random.randint(k_min,k_max)


def random_gaussian(k_min=0, k_max=1):
    return random.randint(0,k_max/2) + random.randint(k_min,k_max/2)
'''
#node attribute: emitter_type --> bursty, periodic, 
#function should define distrubtion knowing min, max in all snapshots

'''
def periodic(k_min=0,k_max=1):
    alt = alternate(k_min,k_max)
    return next(alt)

def alternate(k_min, k_max):
        while True:
            yield 1 #random_gaussian(k_min, k_max)
            yield 0
'''




#for node, edges in self.events.items():
#    times = list(range(self.snapshots))
#    degree = len(edges)
#    event_count = random.randint(1,self.snapshots/2) + random.randint(1,self.snapshots/2) #randomizer function
#    occurences = frozenset( ,k=event_count) )
#for e in tnet.edges.values():
#    count = random.randint(1,steps/2) + random.randint(1,steps/2) #randomizer function
#    occurences = frozenset( random.sample(list(range(steps)),k=count) )
#    tnet.add_edge(e,occurences) 



#def powerlaw(k_min, k_max, y, gamma):
#    return ((k_max**(-gamma+1) - k_min**(-gamma+1))*y  + k_min**(-gamma+1.0))**(1.0/(-gamma + 1.0))