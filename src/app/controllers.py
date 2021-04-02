import eel
#from .stgpy.datasets import Geometric
#from .graphio import json
from .generator.generator_utils import *
from .generator import power_law
from .generator import gaussian
from .generator import uniform
from .generator import geometric
from .serializer import network_writer
from .analyzer.network_measures import *
from .visualizer.draw_measures import *
import os
import glob

"""
@eel.expose 
def createSST():
    print('Python: createSST')
    Geometric.buildNodeMovementDataset()
    json.writeAllJSONs('out_node-00-00')
"""

tnets = {}
counter = 1

@eel.expose
def generate(args): 
    global counter
    isForced =True if args['nodes_velocity'] == 'dynamic' else False
    print("Hello World")
    if args['degree_distribution'] == "geometric":
        #print("not implemented")
        shutil.rmtree('out_node-00-00', ignore_errors=True)
        sstLauncher.buildNodeMovementDataset(r=float(args['radius']), nodes=int(args['nodes_count']), duration=int(args['frames_count']), std=float(args['std']), mean=float(args['mean'])  )
        g = dat.loadAllGraphs('out_node-00-00')
        tnet = TemporalNetwork()
        getGeometricNodes(tnet, g)
        getGeometricEdges(tnet, g)
        print_tnet(tnet)
        tnets[counter] = tnet
        counter+=1
        #TODO Testing only - need to track position over time with nodes
        from app.serializer import json
        json.writeAllJSONs('out_node-00-00')
    elif args['degree_distribution']== "powerlaw":
        tnet = power_law.generate(int(args['nodes_count']), float(args['kmin']), float(args['kmax']), float(args['gamma']), isForced)
        e = Event_Scheduler(tnet, int(args['frames_count']))
        e.execute(args)
        #evolve(tnet, int(args['frames']), .5)
        tnets[counter] = tnet
        counter+=1
        #writer.save_json(tnet,name='powerlaw',start=0,end=args.frames) 
    elif args['degree_distribution'] == "gaussian":
        tnet = gaussian.generate(int(args['nodes_count']), int(args['min_degree']),int(args['max_degree']), isForced)
        e = Event_Scheduler(tnet, int(args['frames_count']))
        e.execute(args)
        #e.static()
        #evolve(tnet, int(args['frames']), .5)
        tnets[counter] = tnet
        counter+=1
        #writer.save_json(tnet,name='gaussian',start=0,end=args.frames)
    elif args['degree_distribution'] == "uniform":
        tnet = uniform.generate(int(args['nodes_count']), int(args['min_degree']),int(args['max_degree']), isForced)
        e = Event_Scheduler(tnet, int(args['frames_count']))
        e.execute(args)
        #e.gaussian()
        #evolve(tnet, int(args['frames']), .5)
        tnets[counter] = tnet
        counter+=1
        #writer.save_json(tnet,name='uniform',start=0,end=args.frames)
    print(tnets)

@eel.expose
def get_tnet(i):
    i = int(i)
    tnet = tnets[i]
    jsons = network_writer.get_jsons(tnet,start=0,end=len(tnet))
    return jsons;

@eel.expose
def get_description(i):
    print("i",i)
    return str(tnets[i])

@eel.expose
def get_count():
    return len(tnets)


@eel.expose
def analyze(index): 
    index = int(index)
    print(tnets[index])
    tnet = tnets[index]
    degrees = temporal_degree_centrality(tnet)
    draw_temporal_degree_centrality(degrees)
    print('degrees')
    degree_totals = temporal_degree_centrality_overall(degrees)
    draw_temporal_degree_centrality_overall(degree_totals)
    print('degree totals')
    overlaps_network = topological_overlap_overall(tnet)
    draw_topological_overlap_overall(overlaps_network)
    print('overlaps-network')
    overlaps_nodes = topological_overlap(tnet)
    draw_topological_overlap(overlaps_nodes)
    print('overlaps-nodes')
    overlap_averages = topological_overlap_average(overlaps_nodes)
    draw_topological_overlap_average(overlap_averages)
    print('overlap averages')
    tcc = temporal_correlation_coefficient(overlap_averages)
    draw_temporal_correlation_coefficient(tcc)
    print('tcc', tcc)
    #New Analysis
    icts = intercontact_times(tnet)
    draw_icts_avg_lag(icts)
    draw_icts_max_lag(icts)
    print('icts',icts)
    edge_coeff = bursty_coeff(icts)
    draw_bursty_coeff(edge_coeff)
    draw_bursty_coeff_avg(edge_coeff)
    print('bursty coeff',edge_coeff)
    lvs = local_variation(icts)
    draw_lvs(lvs)
    draw_lvs_avg(lvs)
    print('lvs', lvs)
    paths = get_shortest_paths(tnet)
    draw_shortest_paths(paths)
    print('paths',paths,0,len(tnet))
    tcc = closeness_centrality(paths)
    draw_closeness(tcc)
    print('tcc', tcc)
    tbc = betweenness_centrality(paths)
    draw_betweenness(tbc)
    print('tbc', tbc)



@eel.expose
def clear_data():
    print('clear data')
    files = glob.glob('./browser/data/*.png')
    for f in files:
        os.remove(f)

"""
def my_other_thread():
    while True:
        print("I'm a thread")
        eel.sleep(1.0)                  # Use eel.sleep(), not time.sleep()

eel.spawn(my_other_thread)
"""


#~~~~~~~[ 2021-03-05 ]~~~~~~~#
import shutil
from .generator.geometric.sst import sstLauncher
from .serializer import dat
from .models.network import *


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

def print_tnet(tnet):
    for n in tnet.nodes.values():
        for t in range(len(tnet)):
            print(n.at_time(t))
    for e in tnet.edges.values():
        print(e)


