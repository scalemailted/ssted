import networkx as nx
import re
from ast import literal_eval as make_tuple
import os

########################################################################################

def loadAllGraphsAtTime(experiments, time):
    graphs = []
    root = "../out_node\\{stddev:02}\\{experiment:02}/{time:02}.dat";
    for i in range(experiments):
        filename = root.format(stddev=0, experiment=i, time=0)
        g = loadGraph(filename)
        graphs.append(g)
    return graphs


def loadAllGraphs(folder):
    graphs = []
    dirlist = os.listdir(folder)
    for filename in dirlist:
        if '.dat' in filename:
            g = loadGraph( folder+'/'+filename)
            graphs.append(g)
    return graphs

#########################################################################################

def loadGraph(filename):
    """reads a graph file and loads into memory"""
    print('Loading {filename}'.format(filename=filename))
    graph = nx.Graph() #nx.DiGraph()
    filedata = open(filename, 'r')
    for row in filedata:
        if 'List' in row:
            parseNode(row, graph)
        elif 'Mag' in row:
            parseEdge(row, graph)
    return graph

def parseNode(string, graph):
    #format:  "$node;[List$pos];\n"
    m = re.match(r'(?P<node>.*);\[List(?P<pos>.*)\];\n', string)
    node, pos = m.group('node'),  make_tuple( m.group('pos') ) 
    graph.add_node(node, pos=pos)

def parseEdge(string, graph):
    #format:  "$uid;($src,$dst);[Mag($weight)];\n"
    m = re.match(r'(?P<uid>.*);\((?P<src>.*),(?P<dst>.*)\);\[Mag\((?P<weight>.*)\)\];\n', string)
    src,dst,weight,uid = m.group('src'), m.group('dst'), float(m.group('weight')), m.group('uid')
    graph.add_edge(src, dst, weight=weight, uid=uid)