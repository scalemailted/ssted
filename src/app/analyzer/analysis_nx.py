import networkx as nx
import numpy as np
import statistics
from itertools import chain
import matplotlib
matplotlib.use('TKAgg')

#Stochastic Spatial Temporal Network Analysis

'''
Non-temporal Analysis
'''

#Global Metric: Assortativity || Degree Correlation
#def getDegreeAssortativity(graph):
#    return nx.degree_assortativity_coefficient(graph)

#Check the parameters for this method --> similarity between nodes
#Default pairwise similarity average
def getPCC(graph):
    return nx.degree_pearson_correlation_coefficient(graph)

def getDegreeConnectivity(graph):
    nodeMap = nx.average_degree_connectivity(graph)
    #return np.mean(list(nodeMap.values()))
    return statistics.mean(nodeMap.values())

#LONG TIME ON G5000!
def getConnectivity(graph):
    return nx.node_connectivity(graph)

#Global Metric: Distance || Geodestics
def getGeodestic(graph):
    #try:
    #    return nx.average_shortest_path_length(graph)
    #except nx.NetworkXNoPath:
    total = 0
    for sg in (graph.subgraph(c) for c in nx.connected_components(graph)):
        total += nx.average_shortest_path_length(sg) * sg.number_of_nodes()
    return total / graph.number_of_nodes()

#LONG TIME ON G5000!
def getShortestPathAvg(g):
    # This includes the isolated node!
    path_lengths = (x[1].values() for x in nx.shortest_path_length(g) )
    return statistics.mean(chain.from_iterable(path_lengths))

'''
def getGeodestic(graph):
    #counts= {}
    total = 0.0
    count = 0
    for n in graph.nodes(): 
        #counts[n]=0
        for j in graph.nodes():
            if (n!=j):
                try:
                    gener=nx.all_shortest_paths(graph,source=n,target=j)
                    total += len(next(nx.all_shortest_paths(graph,n,j))) -1
                    count += 1
                    print(count)
                    #for p in gener:
                    #    for v in p: 
                    #        counts[v]+=1
                except nx.NetworkXNoPath:
                    # do whatever you want
                    continue
    return total/count
'''
'''
connected_components = nx.connected_components(graph)
total = 0
count = 0
for component in connected_components:
    pathMap = nx.average_shortest_path_length(component)
    total += np.mean(list(map(float,pathMap)))
    count += 1
return total / count
'''

#def getDiameter(graph):
#    return nx.diameter(graph)

#Global Metric: Clustering || Connectedness
#def getClusteringCoeff(graph):
#    return nx.clustering(graph)

#LONG TIME ON G5000!
def getClusteringAvg(graph):
    return nx.average_clustering(graph)
    
#def getClusteringSquares(graph): 
#    return nx.square_clustering(graph)

#LONG TIME ON G5000!
def countTriangles(graph):
    triangles = nx.triangles(graph)
    return sum(triangles.values())/3    #each triangle counted 3x

# PowerLaw || kstest
import networkx as nx
from scipy.stats import kstest
import powerlaw

#read what these values should be
def fitPowerLaw(graph):
    deg_dist = sorted([deg for node, deg in graph.degree()], reverse=True)
    fit = powerlaw.Fit(deg_dist, discrete=True)
    alpha = fit.power_law.alpha
    xmin = fit.power_law.xmin
    test, p = kstest(deg_dist, "powerlaw", args = (alpha, xmin),N=len(deg_dist))
    return test, p



'''
Temporal Analysis
'''



'''
from datReader import *
g50 = loadGraph('50.dat')
g500 = loadGraph('500.dat')
g5000 = loadGraph('5000.dat')
from sst_analysis import *
'''

'''
networkList = loadAllGraphs('../dataset/05/out_node\\05\\00')
sublist = networkList[:2]
tnet = createTemporalNetwork(sublist)
print('tnet shape:' ,tnet.netshape)
tnet.network.head(260)

from teneto import networkmeasures
#Work Quickly on g50, t2
networkmeasures.bursty_coeff(tnet)
networkmeasures.fluctuability(tnet)
networkmeasures.intercontacttimes(tnet)
networkmeasures.local_variation(tnet) 
networkmeasures.temporal_degree_centrality(tnet) 
networkmeasures.topological_overlap(tnet)
networkmeasures.volatility(tnet)

#Hangtime on g50, t2 --> author says poor implementation of shortest path
networkmeasures.reachability_latency(tnet)
networkmeasures.shortest_temporal_path(tnet) 
networkmeasures.temporal_betweenness_centrality(tnet) 
networkmeasures.temporal_closeness_centrality(tnet) 
networkmeasures.temporal_efficiency(tnet) 
'''
from teneto import TemporalNetwork
def toTimeMatrix(networkList):
    matrix = np.array([ nx.to_numpy_array(network) for network in networkList ])
    return matrix.transpose()

#tnet.network is a numpy array with (node,node,time) dimensions
def createTemporalNetwork(networkList):
    timeMatrix = toTimeMatrix(networkList)
    print('shape (nodes,nodes,times):',timeMatrix.shape)
    return TemporalNetwork(from_array=timeMatrix, nettype='wd')


#tnet.plot('slice_plot')
#plt.show()
import matplotlib.pyplot as plt
"""
def drawSliceTemporalNetwork(networkList):
    timemat = toTimeMatrix(networkList)
    fig, ax = plt.subplots(1)
    nodesize, _, timesize = timemat.shape
    ax = teneto.plot.slice_plot(timemat, ax, nodelabels=range(nodesize), timelabels=range(timesize), cmap='Set2')
    plt.tight_layout()
    fig.show()
"""

def drawSlicePlot(tnet):
    tnet.plot('slice_plot')
    plt.show()

def drawStackPlot(tnet):
    tnet.plot('graphlet_stack_plot', vminmax=[-1,1], borderwidth=0)
    plt.show()

#tnet.plot('graphlet_stack_plot', vminmax=[-1,1], borderwidth=0)
#plt.show()
"""
def drawStackTemporalNetwork(networkList):
    timemat = toTimeMatrix(networkList)
    fig, ax = plt.subplots(1)
    ax = teneto.plot.graphlet_stack_plot(timemat, ax)
    plt.tight_layout()
    fig.show()
"""


#Avg Geodestic Path (Path Lnegth)
#Centrality: Degree Centrality, Closeness Centrality, Betweeness Centrality
#Network Density
#Graph Randomization

#Avg Temporal Path Length

"""
Defining Metrics:
Degree of Connectivity

Local Metrics:

Global Metrics:
- Connectivity
- Size
- Clustering

Distance Metrics:
-Diameter
-Avg Path Length
-Geodestics

Clustering
"""

"""
Temporal Metrics:

Concept: Shortest Geodestic Path
The minimum number of edges (or sum of edge weights) that it takes for a node to communicate to another node.  

Concept: Shortest Temporal Distance or "Waiting time"
In temporal networks, quantify the time taken for one node to communicate with another node. 
Temporal paths can be measured by calculating either how many edges are traveled or how many time steps are taken. 

Concept: Intercontact Time
The time taken between two nodes with a direct connection.
The intercontact time between two nodes is defined as the temporal difference distinguishing
two consecutive nonzero edges between those nodes. This definition differs from the shortest
temporal path in so far as it only considers direct connections between two nodes

Nodal Measure:  Temporal Centrality
A node’s influence in a temporal network can be calculated in a way akin to degree centrality
in the static case, where the sum of the edges for a node is calculated. The difference from its
static counterpart is that we also sum the number of edges across time.

Nodal Measure:  Temporal Closeness Centrality
A centrality measure that does consider the temporal order is temporal closeness centrality. 
This is an extension of the static closeness centrality, which is the inverse sum of the shortest paths

Edge Measure: Bursts
In temporal network theory, a hallmark of a bursty edge is the
presence of multiple edges with short intercontact times, followed by longer and varying intercontact times. 
In statistical terms, such a process is characterized by a heavy-tailed distribution
of intercontact time probabilities.

Global Measure: Fluctuability
Although centrality measures provide information about the degree of temporal connectivity,
and bursts describe the distribution of the temporal patterns of connectivity at a nodal level,
one might also want to retrieve information about the global state of a temporal network. To
this end, fluctuability aims to quantify the temporal variability of connectivity.

Global Measure: Volatility
One possible global measure of temporal order is how much, on average, the connectivity
between consecutive t-graphlets changes. This indicates how volatile the temporal network is
over time. 

Global Measure: Reachability Latency
Measures of reachability focus on estimating the time taken to “reach” the nodes in a temporal
network. Both the reachability ratio and reachability time are used. The
reachability ratio is the percentage of edges that have a temporal path connecting them. The
reachability time is the average length of all temporal paths. However, when applying reachability to the brain, the two aforementioned measures are not ideal, given the noncontroversial
assumption that any region in the brain, given sufficient time, can reach all other regions.
With this assumption in mind, we define a measure of reachability, reachability latency,
that quantifies the average time it takes for a temporal network to reach an a-priori-defined
reachability ratio. 

Global Measure: Temporal Efficiency
A similar concept is the idea of temporal efficiency. In the static case, efficiency is computed as
the inverse of the average shortest path for all nodes. Temporal efficiency is first calculated at
each time point as the inverse of the average shortest path length for all nodes. Subsequently,
the inverse average shortest path lengths are averaged across time points to obtain an estimate
of global temporal efficiency.

Statistical Considerations of Temporal Network Measures
When implementing temporal graph measures, it is important to perform adequate statistical
tests to infer differences between the subject groups, task conditions, or chance levels. For
group comparisons, nonparametric permutation methods are advantageous where the group
assignment of the calculated measure can be shuffled between the groups and a null distribution can be created. Alternatively, to justify that a measure is significantly present above
chance levels, the construction of null graphs is required. There are multiple ways to create
temporal null graphs, and they each have their own benefits and drawbacks. One method
is to permute the temporal order of entire time series, but this will destroy any autocorrelation present in the data. Another alternative is to permute the phase of the time series prior to
thresholding the t-graphlets. A third option would be to permute blocks of time series data, but
this may not be appropriate for all network measures (e.g., volatility). A fourth option would
be to use vector autoregressive null models (Chang & Glover, 2010; Zalesky et al., 2014). We
refer the reader to Holme & Saramäki (2012) for a full account of approaches to performing
statistical tests on measures derived from temporal network theory.
"""


"""
NETWORK METRICS
Distance Metrics
    - Geodestic Path
    - Avg Geodestic distance
    - Avg Closeness Centrality 
    - Diameter: Largest Geodestic distance

Clustering Metrics
    - Global Clustering Coefficient
    - Local Clustering Coefficient
    - Transitivity ratio
    - Avg Triangles (clustering degree)
    
Degree Correlation Metrics
    - Assortative mixing
    - Disassortative mixing
    - Intraclass correlation
    - Interclass correlation
    - Pearson degree correlation
    - Avg degree of Nearest Neighbor of degree

"""

#Local Metrics
    #Degree of Connectivity
    #Geodestic paths
    #Centrality
        #Closeness
        #Betweeness
        #Prestige

#Global Metrics
    #Connectivity
    #Scale & Size
        #Diameter
    #Clustering

"""
• Networks Overview
    o Network Paradigm
        - Networks are about connectivity
        - Interconnectivity & Correlations
        - The relations between components
        - Geometry of Networks is Topology (different than euclidean distance)
        - Networks often emerge from bottom up approach from local interactions
        - Nonlinearity & Complexity inherit in Networks

    o Networks Analysis
        - What are features of network we care about
        - What are the nodes and the properties we are about
        - Are the relations weighted or not?
        - Are the relations bi-directional?
        - Overall structure of network analysis
            - How connected is it?
            - Are all the nodes connected or are parts disconnected
            - How dense are the connections
            - What are the patterns of clustering in the network?
            - Many small groups or few large groups?
            - If we change a parameter of its structure how will it affect the network
        - Identify different types of networks
            - Networks are not random
                - Designed with top-down, global rules used to create network
                - Designed with bottom-up, local rules used to create components & grow network
        - Network Diffussuion
            - How do things spread across a network
        - Network Dynamics
            - How do network lifecycles occur: form & evolve 

• Graph theory (Local Metrics)
    o Graphs
        - Graphs are node + edges
        - nodes have properties
        - edges are relations between two nodes
        - network is a graph
        - graphs can be directed or undirected in relations
        - edges may have weights on the relations
        - multiplex graphs have different relations for a set of nodes

    o Network Connections
        - Measure significance of a thing in terms a quantity of one of its properities
        - How connected an individual node is, becomes a key metric of its signigficane witin a network
        - Degree of Connectivity
            - The measure of connections a node has to other nodes
            - In & Out Degree
            - Weighted graphs, we can place a quantitative value on each edge
            - Two connected nodes are adjacent
            - Graphs may be represented as an adjacency matrix.
            - Walks: a sequence of adjacent vertices where repetition is allowed
            - Path: a walk without revisiting nay nodes
            - Geodestic: shortest path between two nodes in a graph.
                - represents the fewest number of links that may be traversed to get form one node to another

    o Network Centrality
        - Node Importance: 
            - The measure of how imnfluencial or significant a node is to the overall network
            - The concept of significance will vary for the type of network we are analyzing
            - What characterizes an important node?
        - Degree Connectivity:
            - The node's position with the overall network
            - Number of nodes it is connected to vs. the total it could possibly be connected with
        - Node Signifiacnce
            - Centrality depends on the context
            - Signficance of node depends on two parameters:
                -Quality of flow
                    - How much traffic of network flows through that node
                - Importance Bridge
                    - How critical is that node to the flow
        - Different Centrality Metrics
            - Degree Connectivity
                - Defines nodes significance in its local environment
            - Closeness Centrality
                - How close is the node to other nodes in the nework 
                - How easily can the node reach other nodes in the network
            - Betweeness Centrality
                - Capture the node's role as a connector or bridge between other groups of nodes
            - Prestige Centrality
                - describe how significant a node is based on the significance of the nodess its connected to
            Closeness
                - Defined as a reciprocal of far-ness
                - far-ness is defined as the sum of its distance from all other nodes
                - closeness is a measurement of a node's capacoty to effect all other nodes in the network
            Betweeness
                - nodes that have a high probability of occurring on a random chosen shortest path between two vertices
            Prestige Centrality
                - Eigenvector centrality
                    - assigns relative scores to all nodes in network based on concept
                        connecttions to highly connected nodes contribute more 
                        than connections to nodes with low degrees of connectivity
            
• Network Structure (Global Metrics)
    o Network Topology
        - Network Structure:
            - Networks are very informal type of structure they often develop without any overall top-down design
        - Global & Local
            - Networks may start random but often develop into some stable overall structure
            - Overall structure is of central importance in network theory
        - Topology
            -overll structure of network
            - the way different nodes are placed or interconnected & the overall patterns that emerge out of this
        - Types of Topologies
            - Different network topologies can have different features or properties to them
            - Ring
            - Mesh
            - Star
            - Fully Connected
            - Line
            - Tree
            - Bus
        - Effect of Topology
            - Overall topology feeds back to effect the actions and capabilities of the nodes on the local level
        - Global Features of Network
            - Connectivity
                - The density of the connections in the system
                - How easy or difficult is it for nodes to form a connection
                    - easy:  makes more dense networks
                    - hard: makes sparsely connected or disconnected networks
            - Scale
                - The network size is defined by the number of nodes
                - More is not just more (of same), but in fact can be different (behavior)
            - Clustering
                - A network's overall pattern of connectedness
                - Due to some common set of properties within a set, we get subsystems forming within networks
                - Clusters are the subsytems (subgraphs) within the network
                - Clusters often have a significant effect on the network's makeup
        - Global Structure
            - Networks are often created by nodes in the network who create or don't create connections
              in response to local level conditions but once a network has reached a level of maturity
              a global structure will have emerged to it that feeds back to affect the elements in the 
              system
             - Once this occurs, must analyze the global structure or topology to understand it

    o Connectivity
        - The most defining feature of a network
        - Importance of Network Connectivity
            - Differene betweeen a system with low degree of connectivity vs high degree
                - Quantative change:
                    - The number of edges in the network
                - Qualatative change:
                    -Marks a shift from a components-based regime to a connections-based regime
                        - components-based models & analsizes the subsystems 
                        - connections-based models how the system is interconnected
        - Coupling Parameter
            - Defines how difficult it is for a node in the network to make a connection with another
            - Under what circumstance are the nodes more liekly to interact
            - Set based on a number of different factors
                - distance
                - weight
                - cost
        - Network Density
            - The ratio of the number of edges to the number of possible edges
            - This will correlate to the average degree of connectivity the nodes in the network
                - when we increase the coupling parameter we increase
                    - the density of the network
                    - the average degree of connectivty
                - when we decrease the coupling paranmeter
                    - their will be less connections
                    - more costly to links will be first to go
                    - network could breakdown
        - Proportionality
            - The amount of connectivity in a newtork is defined by how much resources a node must exert
                    - the amount of resources a node must exert to create a connection
                      will grow in proportion to the length of the relation
                        - Not necesssarily linear 
                            - thus level of connectivity can grow or decay in exponentially
    
    o Diameter & Scale
        - Importance of Scale


    o Clustering & Connectedness
• Types Of Networks
    o Degree Distribution
    o Random & Decentralized Networks
    o Decentralized & Small World Networks
    o Centralized & Scale Free Networks
• Network Diffusion
    o Network Dynamics
    o Diffusion & Contagion
    o Robustness
"""

"""
Power Law Distrubtion
kstest
"""