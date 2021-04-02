Strategy:

Step 1:
Generate a static network given a set of parameters
    a. Edge distrubtion (uniform, gaussian, powerlaw, etc)
    b. Node proximity (random, group clustered)
    c. Unigraph/Digraph


Step 2:
Evolve the static network into a delta time networks given a set of paramaters
    a. Edge variances
    b. Node positional/clustering/grouping variances 
    c. Edge Frequency variance i.e. intercontact times (Continuous, Uniform intermittentence, Bursty intermittence)
        - Models: Bandwidth of a Node, how widely can is broadcast within in the network
        - Models: Packet/frame, how often do new edges appear in network
    d. Network growth rate


Progress Report:
1. Start with generating static networks with given parameters
2. Model burstiness in powerlaw network [TODO]
    - Low bandwidth, to high bandwidth, to low bandwidth
3. Refactor Tnet Model  
    nodes --> set for all time slices
    edges --> set for all time slices
                -->  each edge has list of time stamps
    time --> time data
            start time --> time of first slice
            end time --> time of second slice
            delta time --> duration between time steps

4. 
nodal degree distrubtion
    powerlaw
    gaussian
    uniform

edge temporal frequency:
    Bursty --> ict lag before update (frames)
    Random --> ict lag before upate (frames)
    Periodic --> ict lag before update (frames)

node placement:
    k-means cluster
    random 

node motion:
    fixed
    velocity


Model:
Tnet
    nodes set   
    edges set
    frame_count

node
    id, pos

edge
    src, dst, occureneces


#TODO
Edge class: 
    +new attributes:
    occurenece_type --> used by: evolve method
                    --> options: periodic, bursty, random
                    --> default: 'random'

Node class: 
    +new attributes:
    broadcast_type --> used by: evolve method
                   --> options: burtsy, periodic, random, constant
                   --> default: 'random'

    max_degree     --> used by: evolve method
                   --> set by: tnet
    
    event_times    --> used by: evolve method
                   --> set by: tnet, tnet.occurenece_type, tnet.max_degree

Scheduler class: (NEW)
    dict --> node: edges
    logic that defines a node broadcast type and an edge icts 

    cascading effect: event passed betweeb nodes

from collections import defaultdict
class Scheduler:
    def __init__(self, tnet):
        self.tnet = tnet
        self.events = defaultdict(set)
    def add_events(self, node, edges):
        self.events[node] |= edges;
    def setup(self):
        for 
    def execute(self):
        
    def __len__(self):
        return len(self.events)
    def __str__(self):
        return "Scheduler, events:" 

spawn an event broadcast across network
ttl
length in time
repawn rate from origin

'''

tnet = generate()                           # running the new Model
e = Event_Scheduler(tnet,10)
e.gaussian()
print(tnet)
save_json(tnet, 'event-schedule',0,9)

'''

'''
>>> def generate(nodes=100, k_min=1.0, k_max=100, gamma=3.0):
...     degree_list = generate_degrees(powerlaw, nodes, k_min, k_max, gamma)
...     edge_list = generate_edges(degree_list)
...     tnet = generate_tnet(edge_list)
...     return tnet
'''
