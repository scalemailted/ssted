from ..models.network import *

import os


#TODO: Refactor to only having writing logic

def save_json(tnet, name='tnet', start=0, end=30):
    dirName = f"{name}-{start}-{end}"
    os.mkdir(dirName)
    for time in range(start, end):
        path = os.path.join(dirName, f"{time:02d}.json")
        json = open(path,'w')
        nodes, edges = tnet.get(time,time+1)
        g = StaticNetwork(nodes, edges)
        g_string = str(g)
        print("Writing file")
        json.write(g_string)
        json.flush()
        json.close()
        print("File written")

#Updated 2021-3-5 for tnodes
def get_jsons(tnet, name='tnet', start=0, end=30):
    jsons = []
    for time in range(start, end):
        nodes, edges = tnet.get(time,time+1)
        print('nodes',nodes)
        if isinstance(list(nodes)[0], TemporalNode):
            tnodes = []
            for n in nodes:
                tnodes.append(n.at_time(time))
            nodes = tnodes
        g = StaticNetwork(nodes, edges)
        g_string = str(g)
        jsons.append(g_string)
    return jsons