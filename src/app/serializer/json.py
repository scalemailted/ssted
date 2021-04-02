import networkx as nx
import re
from ast import literal_eval as make_tuple
import os


#########################################################################################

def readDatGraph(filename):
    """reads a graph file and loads into memory"""
    print(f'Loading {filename}')
    graph = nx.Graph() #nx.DiGraph()
    filedata = open(filename, 'r')
    nodes, edges = [], []
    for row in filedata:
        if 'List' in row:
            n = parseNode(row, graph)
            nodes.append(n)
        elif 'Mag' in row:
            e = parseEdge(row, graph)
            edges.append(e)
    return nodes, edges

def parseNode(string, graph):
    #format:  "$node;[List$pos];\n"
    m = re.match(r'(?P<node>.*);\[List(?P<pos>.*)\];\n', string)
    node, pos = m.group('node'),  make_tuple( m.group('pos') ) 
    return node ,pos

def parseEdge(string, graph):
    #format:  "$uid;($src,$dst);[Mag($weight)];\n"
    m = re.match(r'(?P<uid>.*);\((?P<src>.*),(?P<dst>.*)\);\[Mag\((?P<weight>.*)\)\];\n', string)
    src,dst,weight,uid = m.group('src'), m.group('dst'), float(m.group('weight')), m.group('uid')
    return src, dst, weight ,uid

def jsonifyNode(id, pos, group=1):
    #return f'{{"id": "{id}", "group": {group}}}'
    return f'{{"id": "{id}", "fx": {pos[0]}, "fy": {pos[1]}, "group": {group}}}'

def jsonifyEdge(src, dst, weight):
    return f'{{"source": "{src}", "target": "{dst}", "value": {weight}}}'

def jsonifyGraph(nodes,edges):
    nodes = [ jsonifyNode(uid,pos) for (uid,pos) in nodes ]
    edges = [ jsonifyEdge(src,dst,weight) for (src,dst,weight,uid) in edges ]
    return f'{{"nodes": [{",".join(nodes)}], "links": [{",".join(edges)}]}}'

def writeJSON(filename, jsonname='out'):
    nodes, edges = readDatGraph(filename)
    json = jsonifyGraph(nodes, edges)
    jsonfile = open(f'{jsonname}.json', 'w')
    jsonfile.write(json)
    jsonfile.close()
    print(f'{jsonname}.json written')

def writeAllJSONs(folder):
    dirlist = os.listdir(folder)
    for filename in dirlist:
        if '.dat' in filename:
            outname = filename.replace('.dat','')
            writeJSON( folder+'/'+filename, folder+'/'+outname)
