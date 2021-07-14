from ..models.network import *
import os
import json

import networkx as nx
import re
from ast import literal_eval as make_tuple

########################################################################################

def loadAllGraphs(folder):
    t = 0
    tnet = TemporalNetwork()
    dirlist = sorted(os.listdir(folder))
    for filename in dirlist:
        if '.json' in filename:
            loadGraph( tnet, folder+'/'+filename, t)
            t += 1
    return tnet

#########################################################################################

def loadGraph(tnet, filename,t):
    """reads a graph file and loads into memory"""
    print('Loading {filename}'.format(filename=filename))
    #graph = nx.Graph() #nx.DiGraph()
    filedata = open(filename, 'r')
    data = json.load(filedata)
    for node in data['nodes']:
        #print(node)
        n,x,y,grp = node['id'], node['fx'], node['fy'], node['group']
        pos = Position(x,y)
        tnet.add_node(n,pos,grp)
    for link in data['links']:
        #print(link)
        src, dst = link['source'], link['target']
        te = TemporalEdge(src,dst,t)
        tnet.add_edge_without_nodes(te)
    '''
    for row in filedata:
        if 'List' in row:
            parseNode(row, graph)
        elif 'Mag' in row:
            parseEdge(row, graph)
    return graph
    '''


###################################################################################################

def getGeometricNodes(tnet, g):
    t = 0
    for net in g:
        for n in net.nodes:
            x,y = net.nodes[n]['pos']
            pos = Position(x,y)
            tnet.add_tnode(n,pos,t)
        t+=1

def getGeometricEdges(tnet, g):
    t = 0;
    for net in g:
        for e in net.edges:
            src, dst = e
            te = TemporalEdge(src,dst,t)
            tnet.add_edge_without_nodes(te)
            print(te.id)
        t+=1





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