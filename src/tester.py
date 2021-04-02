from app.controllers import * 

args = {'degree_distribution':'uniform',
        'nodes_count':50,
        'min_degree':0, 
        'max_degree':6,
        'frames_count':10,
        'isForced':False, 
        'nodes_velocity':0,
        'emitter_type':'uniform', 
        'events_min_rate':0, 
        'events_duration':1, 
        'events_activity_rate':1
    }

def intercontact_times(tnet):
    print("computing... intercontact times")
    icts = {}
    prev_t = {}
    for t in range(len(tnet)):
        g, edges = tnet.get(t,t+1)
        #edges = g.edges.keys()
        for e in edges:
            if not icts.get(e):
                #icts[e] = [t]
                icts[e] = [t or 1]
                prev_t[e] = t
            else:
                #icts.append(t)
                icts[e].append( t - prev_t[e] )
                prev_t[e] = t
    return icts

def bursty_coeff(icts):
    edge_coeff = {}
    for i in icts:
        edge_coeff[i] = (np.std(icts[i]) - np.mean(icts[i])) / (np.std(icts[i]) + np.mean(icts[i]))
    return edge_coeff

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


def main():
    generate(args)
    tnet = tnets[1]
    icts = intercontact_times(tnet)
    print('icts',icts)
    edge_coeff = bursty_coeff(icts)
    print('edge coeff',edge_coeff)
    lvs = local_variation(icts)
    print('lvs',lvs)
    paths = get_shortest_paths(tnet)
    print('paths',paths)

#main()





import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from matplotlib.ticker import MaxNLocator

#Complete!
def draw_icts_avg_lag(icts):
    ax = plt.figure().gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True)) #set xaxis to int
    vals = defaultdict(lambda: 0)
    for i in icts.values():
        vals[round(np.average(i),1)]+= 1
    #avg_lags = [ round(np.average(i),1) for i in icts.values()  ]
    x_vals,y_vals = zip(*sorted(vals.items()))
    #plt.ylim((-.1,1.1))
    plt.plot(x_vals, y_vals, '-o')
    plt.xlabel('Average tween-time (in frames)')
    plt.ylabel('Edge Count')
    plt.title('Intercontact Time - Edge Measure')
    plt.show()

#Complete!
def draw_icts_max_lag(icts):
    ax = plt.figure().gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True)) #set xaxis to int
    vals = defaultdict(lambda: 0)
    for i in icts.values():
        vals[max(i)]+= 1
    #max_lags = [ max(i) for i in icts.values()  ]
    x_vals,y_vals = zip(*sorted(vals.items()))
    #plt.ylim((-.1,1.1))
    plt.plot(x_vals, y_vals, '-o')
    plt.xlabel('Max tween-time (in frames)')
    plt.ylabel('Edge Count')
    plt.title('Intercontact Time - Edge Measure')
    plt.show()

#Complete!
def draw_bursty_coeff(edge_coeff):
    ax = plt.figure().gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True)) #set xaxis to int
    vals = defaultdict(lambda: 0)
    for i in edge_coeff.values():
        vals[round(i,1)]+= 1
    #max_lags = [ max(i) for i in icts.values()  ]
    x_vals,y_vals = zip(*sorted(vals.items()))
    #plt.ylim((-.1,1.1))
    plt.plot(x_vals, y_vals, '-o')
    plt.xlabel('Bursty Coeff')
    plt.ylabel('Edge Count')
    plt.title('Bursty Coeff - Per Edge Measure')
    plt.show()


#Complete
def draw_bursty_coeff_avg(edge_coeff):
    avg_coeff = np.average(list(edge_coeff.values()))
    x_vals = [0,1]
    y_vals = [avg_coeff,avg_coeff]
    plt.ylim((-1.1,1.1))
    plt.xlim((.1,.9))
    plt.gca().axes.xaxis.set_visible(False)
    plt.plot(x_vals, y_vals, 'r')
    plt.text(0.45, avg_coeff+0.04, " "+str(round(avg_coeff,3)), color='black', va='center', fontweight='bold')
    #plt.plot(x_vals, y_vals, '-r')
    plt.ylabel('Bursty Coeff Avg')
    plt.title('Average Bursty Coeff - Network Measure')
    plt.show()

#Complete
def draw_lvs(lvs):
    ax = plt.figure().gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True)) #set xaxis to int
    vals = defaultdict(lambda: 0)
    for i in lvs.values():
        vals[round(i,1)]+= 1
    #max_lags = [ max(i) for i in icts.values()  ]
    x_vals,y_vals = zip(*sorted(vals.items()))
    #plt.ylim((-.1,1.1))
    plt.plot(x_vals, y_vals, '-o')
    plt.xlabel('Local Variation')
    plt.ylabel('Edge Count')
    plt.title('Local Variations - Per Edge Measure')
    plt.show()

#Complete
def draw_lvs_avg(lvs):
    avg_lvs = np.average(list(lvs.values()))
    x_vals = [0,1]
    y_vals = [avg_lvs,avg_lvs]
    plt.gca().axes.xaxis.set_visible(False)
    plt.plot(x_vals, y_vals, 'r')
    plt.text(0.45, avg_lvs+0.04, " "+str(round(avg_lvs,3)), color='black', va='center', fontweight='bold')
    #plt.plot(x_vals, y_vals, '-r')
    plt.ylabel('Local Variation Avg')
    plt.title('Average Local Variation - Network Measure')
    plt.show()

def draw_shortest_paths(path_data):
    vals = defaultdict(lambda: 0)
    for key in path_data:
        delta = path_data[key]['delta'].values()
        #print( len(delta) )
        vals[len(delta)] += 1
    x_vals,y_vals = zip(*sorted(vals.items()))
    #plt.ylim((-.1,1.1))
    plt.plot(x_vals, y_vals, '-o')
    plt.xlabel('Node Reachability Score')
    plt.ylabel('Node Count')
    plt.title('Reachable Nodes')
    plt.show()


##############################################
# Feb 18

#TODO BUG Generate doesn't create specified number of nodes. Requested 50 nodes, less than 50 in geenrated network

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


#Visualizations
def draw_betweenness(betweenness):
    x_vals = [0]* len(betweenness)
    y_vals = list(betweenness.values())
    plt.ylim((-.1,1.1))
    plt.gca().axes.xaxis.set_visible(False)
    plt.plot(x_vals, y_vals, 'or', alpha=0.05)
    plt.xlabel('Temporal Betweenness Centrality')
    plt.ylabel('TBC %')
    plt.title('Temporal Betweenness Centrality - Node Measure')
    #plt.show()
    plt.savefig('./browser/data/tbc.png')
    plt.close()



def draw_closeness(closeness):
    x_vals = [0]* len(closeness)
    y_vals = list(closeness.values())
    plt.ylim((-.1,1.1))
    plt.gca().axes.xaxis.set_visible(False)
    plt.plot(x_vals, y_vals, 'or', alpha=0.05)
    plt.xlabel('Temporal Closeness Centrality')
    plt.ylabel('TCC %')
    plt.title('Temporal Closeness Centrality - Node Measure')
    #plt.show()
    plt.savefig('./browser/data/tcc.png')
    plt.close()