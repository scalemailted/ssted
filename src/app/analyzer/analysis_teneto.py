'''
[ Script Overview ]:
This script sets up a generated temporal network to:
    - convert into a teneto adjacency matrice
    - executes the teneto measures

[ Use case in Research]:
Use this for a comparison between my measures & teneto's
    - time performance      (i.e. how quickly a solution is derived)
    - precision performance (i.e. how the computed measures vary)

[ Launch ]: 
> python3 temporal-analysis.py

'''


import networkx as nx
import numpy as np
import os
import re
from ast import literal_eval as make_tuple
from teneto import TemporalNetwork
from teneto import networkmeasures


def main():
    print('Loading network data')
    networkArray = loadAllGraphs('./data/')
    print('making temporal network')
    tnet = createTemporalNetwork(networkArray)
    print('tnet shape:', tnet.netshape)
    print('calculating shortest path')
    networkmeasures.shortest_temporal_path(tnet) 


#######################################################
#  Converts networkx graph into temporal network
######################################################

# Requires: An array of networkx graphs
# Returns: NP Array of NP Arrays
def toTimeMatrix(networkList):
    matrix = np.array([ nx.to_numpy_array(network) for network in networkList ])
    return matrix.transpose()


# Requires: An array of network graphs
# Returns: Temporal Network
def createTemporalNetwork(networkList):
    timeMatrix = toTimeMatrix(networkList)
    print('shape (nodes,nodes,times):',timeMatrix.shape)
    return TemporalNetwork(from_array=timeMatrix, nettype='wd')


#######################################################
#  .DAT FILE READER FUNCTIONS
######################################################

# Requires: A folder containing DAT files
# Returns: An array of networkx Graphs
def loadAllGraphs(folder):
    graphs = []
    dirlist = os.listdir(folder)
    for filename in dirlist:
        if '.dat' in filename:
            g = loadGraph( folder+'/'+filename)
            graphs.append(g)
    return graphs

#Requires: A filename of a DAT file
#Returns: A networkx Graph
def loadGraph(filename):
    """reads a graph file and loads into memory"""
    print('Loading {filename}'.format(filename=filename))
    graph = nx.Graph() 
    filedata = open(filename, 'r')
    for row in filedata:
        if 'List' in row:
            parseNode(row, graph)
        elif 'Mag' in row:
            parseEdge(row, graph)
    return graph

#Requires: A string & a graph instance
#Returns: none
def parseNode(string, graph):
    m = re.match(r'(?P<node>.*);\[List(?P<pos>.*)\];\n', string)
    node, pos = m.group('node'),  make_tuple( m.group('pos') ) 
    graph.add_node(node, pos=pos)

#Requires: A string & a graph instance
#Returns: none
def parseEdge(string, graph):
    m = re.match(r'(?P<uid>.*);\((?P<src>.*),(?P<dst>.*)\);\[Mag\((?P<weight>.*)\)\];\n', string)
    src,dst,weight,uid = m.group('src'), m.group('dst'), float(m.group('weight')), m.group('uid')
    graph.add_edge(src, dst, weight=weight, uid=uid)



if __name__ == "__main__":
    main()



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











